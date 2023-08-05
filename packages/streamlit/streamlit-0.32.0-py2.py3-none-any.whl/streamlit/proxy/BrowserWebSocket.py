# Copyright 2018 Streamlit Inc. All rights reserved.

"""Websocket handler class for connections to the browser."""

# Python 2/3 compatibility
from __future__ import print_function, division, unicode_literals, absolute_import
from streamlit.compatibility import setup_2_3_shims
setup_2_3_shims(globals())

from tornado import gen
from tornado.concurrent import futures
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketClosedError
from tornado.websocket import WebSocketHandler

from streamlit import __version__
from streamlit import caching
from streamlit import config
from streamlit import protobuf
from streamlit import process_runner
from streamlit.proxy import Proxy
from streamlit.proxy import proxy_util

from streamlit.logger import get_logger
LOGGER = get_logger(__name__)


class BrowserWebSocket(WebSocketHandler):
    """Websocket handler class which the web client connects to."""

    executor = futures.ThreadPoolExecutor(5)

    def initialize(self, proxy):
        """Initialize self._connections."""
        self._proxy = proxy
        self._connection = None
        self._queue = None
        self._is_open = False

    def check_origin(self, origin):
        """Set up CORS."""
        return proxy_util.url_is_from_allowed_origins(origin)

    @Proxy.stop_proxy_on_exception(is_coroutine=True)
    @gen.coroutine
    def open(self, report_name):
        """Get and return websocket."""
        # Indicate that the websocket is open.
        self._is_open = True

        # Get the report name from the url
        self._report_name = report_name
        LOGGER.debug('The Report name is "%s"', self._report_name)

        try:
            LOGGER.debug(
                'Browser websocket opened for "%s"', self._report_name)

            # Get a ProxyConnection object to coordinate sending deltas over
            # this report name.
            self._connection, self._queue = (
                yield self._proxy.on_browser_connection_opened(
                    self._get_key(), self._report_name, self))
            LOGGER.debug('Got a new connection ("%s") : %s',
                         self._connection.name, self._connection)
            LOGGER.debug('Got a new command line ("%s") : %s',
                         self._connection.name, self._connection.command_line)
            LOGGER.debug('Got a new queue : "%s"', self._queue)

            # Send the opening message. self._connection must be
            # set before this is called.
            self._send_new_connection_msg()

            LOGGER.debug('Starting loop for "%s"', self._connection.name)
            loop = IOLoop.current()
            loop.spawn_callback(self.do_loop)

        except KeyError as e:
            LOGGER.debug(
                'Browser attempting to access non-existant report "%s"', e)
        except WebSocketClosedError:
            pass

    @Proxy.stop_proxy_on_exception(is_coroutine=True)
    @gen.coroutine
    def do_loop(self):
        """Start the proxy's main loop."""
        # How long we wait between sending more data.
        throttle_secs = config.get_option('client.throttleSecs')

        indicated_closed = False

        try:
            while self._is_open:
                self._connection, self._queue = (
                    yield self._proxy.get_latest_connection_and_queue(
                            self._report_name, self,
                            self._connection, self._queue))
                if not self._queue.is_closed():
                    yield self._queue.flush_queue(self)
                elif not indicated_closed:
                    LOGGER.debug(
                        'The queue for "%s" is closed.',
                        self._connection.name)
                    indicated_closed = True

                yield gen.sleep(throttle_secs)
            LOGGER.debug('Closing loop for "%s"', self._connection.name)
        except KeyError as e:
            LOGGER.debug(
                'Browser attempting to access non-existant report "%s"', e)
        except WebSocketClosedError:
            pass

        if self._connection is not None:
            self._proxy.on_browser_connection_closed(
                self._get_key(), self._connection, self._queue)

    def _get_key(self):
        """Return a key that uniquely identifies this WebSocket connection."""
        return str(self)

    @Proxy.stop_proxy_on_exception()
    def on_close(self):
        """Close handler."""
        LOGGER.debug('Received close message.')
        self._is_open = False

    @Proxy.stop_proxy_on_exception(is_coroutine=True)
    @gen.coroutine
    def on_message(self, msg):
        """Run callback for websocket messages."""
        LOGGER.debug(repr(msg))
        yield self._handle_backend_msg(msg, self._connection, self)

    @gen.coroutine
    def _send_new_connection_msg(self):
        """Send message to browser with client configuration settings."""
        msg = protobuf.ForwardMsg()

        msg.new_connection.sharing_enabled = (
            config.get_option('global.sharingMode') != 'off')

        msg.new_connection.gather_usage_stats = (
            config.get_option('browser.gatherUsageStats'))

        msg.new_connection.run_on_save = (
            self._proxy.get_run_on_save(self._connection))

        msg.new_connection.streamlit_version = __version__

        LOGGER.debug(
            'New browser connection:\n'
            '\tsharing_enabled=%s\n'
            '\tgather_usage_stats=%s\n'
            '\trun_on_save=%s',
            msg.new_connection.sharing_enabled,
            msg.new_connection.gather_usage_stats,
            msg.new_connection.run_on_save)

        yield self.write_message(msg.SerializeToString(), binary=True)

    @gen.coroutine
    def _handle_backend_msg(self, payload, connection, ws):
        backend_msg = protobuf.BackMsg()
        try:
            backend_msg.ParseFromString(payload)
            LOGGER.debug('Received the following backend message:')
            LOGGER.debug(backend_msg)
            msg_type = backend_msg.WhichOneof('type')
            if msg_type == 'cloud_upload':
                yield self._save_cloud(connection, ws)
            elif msg_type == 'rerun_script':
                yield self._run(backend_msg.rerun_script)
            elif msg_type == 'clear_cache':
                # Setting verbose=True causes clear_cache to print to stdout.
                # Since this command was initiated from the browser, the user
                # doesn't need to see the results of the command in their
                # terminal.
                caching.clear_cache(verbose=False)
            elif msg_type == 'set_run_on_save':
                self._proxy.set_run_on_save(
                    self._connection, backend_msg.set_run_on_save)
            else:
                LOGGER.warning('No handler for "%s"', msg_type)
        except Exception as e:
            LOGGER.error('Cannot parse binary message: %s', e)

    @run_on_executor
    def _run(self, cmd):
        process_runner.run_handling_errors_in_subprocess(
            cmd, self._connection.cwd)

    @gen.coroutine
    def _save_cloud(self, connection, ws):
        """Save serialized version of report deltas to the cloud."""
        @gen.coroutine
        def progress(percent):
            progress_msg = protobuf.ForwardMsg()
            progress_msg.upload_report_progress = percent
            yield ws.write_message(
                progress_msg.SerializeToString(), binary=True)

        # Indicate that the save is starting.
        try:
            yield progress(0)

            files = connection.serialize_final_report_to_files()
            storage = self._proxy.get_storage()
            url = yield storage.save_report_files(
                connection.id, files, progress)

            # Indicate that the save is done.
            progress_msg = protobuf.ForwardMsg()
            progress_msg.report_uploaded = url
            yield ws.write_message(
                progress_msg.SerializeToString(), binary=True)
        except Exception as e:
            # Horrible hack to show something if something breaks.
            err_msg = '%s: %s' % (
                type(e).__name__, str(e) or "No further details.")
            progress_msg = protobuf.ForwardMsg()
            progress_msg.report_uploaded = err_msg
            yield ws.write_message(
                progress_msg.SerializeToString(), binary=True)
            raise e
