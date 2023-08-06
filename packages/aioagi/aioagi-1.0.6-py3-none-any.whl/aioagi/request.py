from aiohttp import FlowControlDataQueue
from aiohttp.helpers import reify

from aioagi.agi_writer import AGIPayloadWriter

from aioagi.parser import AGIRequestMessage
from aioagi.protocol import AGIRequestHandler


class AGIRequest:
    def __init__(self,
                 message: AGIRequestMessage, protocol: AGIRequestHandler,
                 reader: FlowControlDataQueue, writer: AGIPayloadWriter):
        from aioagi.agi import AGI

        self.headers = self._headers = message.headers
        self.method = self._method = message.method
        self.rel_url = self._rel_url = message.url

        self.message = message
        self.protocol = protocol
        self.reader = reader
        self.writer = writer

        self._match_info = None
        self._cache = {}

        self.agi = AGI(self)

    @property
    def match_info(self):
        """Result of route resolving."""
        return self._match_info

    @property
    def transport(self):
        if self.protocol is None:
            return None
        return self.protocol.transport

    @reify
    def app(self):
        """Application instance."""
        return self._match_info.apps[-1]

    @reify
    def path(self):
        return self._rel_url.path

    @reify
    def path_qs(self):
        return str(self._rel_url)

    @reify
    def remote(self):
        """Remote IP of client initiated AGI request.

        The IP is resolved in this order:

        - overridden value by .clone(remote=new_remote) call.
        - peername of opened socket
        """
        if self.transport is None:
            return None
        peername = self.transport.get_extra_info('peername')
        if isinstance(peername, (list, tuple)):
            return peername[0]
        else:
            return peername
