from functools import partial

from aiohttp.web import Application
from aiohttp.abc import AbstractAccessLogger

from aioagi.log import agi_app_logger
from aioagi.server import AGIServer
from aioagi.request import AGIRequest
from aioagi.helpers import AGIAccessLogger
from aioagi.urldispathcer import AGIUrlDispatcher


class AGIApplication(Application):
    server_cls = AGIServer

    def __init__(self, logger=agi_app_logger, **kwargs):
        kwargs.update(router=AGIUrlDispatcher())
        super().__init__(logger=logger, **kwargs)

    def _make_request(self, message, payload, protocol, writer, task,
                      _cls=AGIRequest):
        return _cls(message, payload, protocol, writer)

    def _make_handler(self,
                      loop=None,
                      access_log_class=AGIAccessLogger,
                      **kwargs):

        if not issubclass(access_log_class, AbstractAccessLogger):
            raise TypeError(
                'access_log_class must be subclass of '
                'aiohttp.abc.AbstractAccessLogger, got {}'.format(
                    access_log_class))

        self._set_loop(loop)
        self.freeze()

        kwargs['debug'] = self.debug
        if self._handler_args:
            for k, v in self._handler_args.items():
                kwargs[k] = v

        return self.server_cls(self._handle, request_factory=self._make_request,
                               access_log_class=access_log_class,
                               loop=self.loop, **kwargs)

    async def _handle(self, request):
        match_info = await self._router.resolve(request)
        match_info.add_app(self)
        match_info.freeze()

        request._match_info = match_info
        handler = match_info.handler

        if self._run_middlewares:
            for app in match_info.apps[::-1]:
                for m, new_style in app._middlewares_handlers:
                    if new_style:
                        handler = partial(m, handler=handler)
                    else:
                        handler = await m(app, handler)

        resp = await handler(request)

        return resp
