from aiohttp.web_server import Server

from aioagi.protocol import AGIRequestHandler


class AGIServer(Server):
    def __call__(self):
        return AGIRequestHandler(self, loop=self._loop, **self._kwargs)
