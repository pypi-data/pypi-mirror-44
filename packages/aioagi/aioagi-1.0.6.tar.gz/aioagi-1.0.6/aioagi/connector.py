import functools

from aioagi.client_proto import AGIResponseHandler
from aiohttp import TCPConnector


class AGITCPConnector(TCPConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._factory = functools.partial(AGIResponseHandler, loop=self._loop)
