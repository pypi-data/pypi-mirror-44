from aiohttp.web_urldispatcher import UrlDispatcher, MatchInfoError

from aiohttp import web

from aioagi.hdrs import AGIMethod
from aioagi.exceptions import AGIMethodNotAllowed, AGINotFound
from aioagi.request import AGIRequest


class AGIUrlDispatcher(UrlDispatcher):
    async def resolve(self, request: AGIRequest):
        allowed_methods = set()

        for resource in self._resources:
            match_dict, allowed = await resource.resolve(request)
            if match_dict is not None:
                return match_dict
            else:
                allowed_methods |= allowed
        else:
            if allowed_methods:
                return MatchInfoError(AGIMethodNotAllowed(
                    message='{}: {}'.format(request.method, allowed_methods)))
            else:
                return MatchInfoError(AGINotFound())


class AGIView(web.View):
    def __init__(self, request: AGIRequest):
        self.agi = request.agi
        super().__init__(request)

    async def _iter(self):
        if self.request.method not in AGIMethod.all():
            self._raise_allowed_methods()

        method = getattr(self, self.request.method.lower(), None)
        if method is None:
            self._raise_allowed_methods()
        return await method()

    def _raise_allowed_methods(self):
        allowed_methods = {m for m in AGIMethod.all() if hasattr(self, m.lower())}
        raise AGIMethodNotAllowed(message='{}: {}'.format(self.request.method, allowed_methods))
