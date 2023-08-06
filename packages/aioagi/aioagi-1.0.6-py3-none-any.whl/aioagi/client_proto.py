from aiohttp.base_protocol import BaseProtocol
from aiohttp.client_proto import ResponseHandler

from aioagi.log import agi_client_logger


class AGIResponseHandler(ResponseHandler):
    def __init__(self, *, loop=None):
        super().__init__(loop=loop)

        self._payload = None
        self._payload_parser = None

    def connection_lost(self, exc):
        if self._payload_parser is not None:
            try:
                self._payload_parser.feed_eof()
            except Exception:
                pass

        self.transport = self.writer = None
        self._should_close = True
        self._parser = None
        self._payload = None
        self._payload_parser = None
        self._reading_paused = False

        BaseProtocol.connection_lost(self, exc)

    def data_received(self, data):
        if not data:
            return

        if self._payload_parser is None:
            self._tail += data

        else:
            try:
                self._payload_parser.feed_data(data)
            except Exception as exc:
                agi_client_logger.exception('Command parser error.', exc_info=exc)
                self._should_close = True
                self.transport.close()
                self.set_exception(exc)
                return
