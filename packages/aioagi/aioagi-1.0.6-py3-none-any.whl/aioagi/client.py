import asyncio
import warnings

from yarl import URL

from aiohttp import ClientTimeout
from aiohttp.helpers import sentinel
from aiohttp.client import DEFAULT_TIMEOUT

from aioagi.hdrs import AGIMethod
from aioagi.connector import AGITCPConnector
from aioagi.client_exceptions import AGIInvalidURL, AGIInvalidMethod
from aioagi.client_reqrep import AGIClientRequest, AGIClientResponse


class AGIClientSession:
    def __init__(self, *, connector=None, loop=None,
                 headers=None,
                 request_class=AGIClientRequest, response_class=AGIClientResponse,
                 connector_owner=True, raise_for_status=False,
                 timeout=None):

        if loop is None:
            loop = asyncio.get_event_loop()

        self._loop = loop

        if connector is None:
            connector = AGITCPConnector(loop=self._loop)

        self._connector = connector
        self._connector_owner = connector_owner

        self._timeout = timeout or DEFAULT_TIMEOUT
        self._raise_for_status = raise_for_status

        self._default_headers = headers or {}

        self._request_class = request_class
        self._response_class = response_class

    def __del__(self, _warnings=warnings):
        if not self.closed:
            self._connector.close()

            _warnings.warn("Unclosed client session {!r}".format(self),
                           ResourceWarning)
            context = {'client_session': self,
                       'message': 'Unclosed client session'}

            self._loop.call_exception_handler(context)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def request(self, method, url, *, params=None, headers=None, timeout=sentinel):
        if not isinstance(method, AGIMethod):
            try:
                method = AGIMethod(method)
            except ValueError:
                raise AGIInvalidMethod(method)

        try:
            url = URL(url)
        except ValueError:
            raise AGIInvalidURL(url)

        url = url.with_fragment(None)

        request_headers = self._default_headers.copy()
        headers and request_headers.update(headers)

        if timeout is sentinel:
            timeout = self._timeout
        else:
            if not isinstance(timeout, ClientTimeout):
                timeout = ClientTimeout(total=timeout)

        return self._request_class(
            method, url,
            params=params, headers=request_headers,
            timeout=timeout, response_class=self._response_class,
            session=self, loop=self._loop)

    def local(self, url, **kwargs):
        return self.request(AGIMethod.LOCAL, url, **kwargs)

    def sip(self, url, **kwargs):
        return self.request(AGIMethod.SIP, url, **kwargs)

    def dahdi(self, url, **kwargs):
        return self.request(AGIMethod.DAHDI, url, **kwargs)

    def iax2(self, url, **kwargs):
        return self.request(AGIMethod.IAX2, url, **kwargs)

    def motif(self, url, **kwargs):
        return self.request(AGIMethod.MOTIF, url, **kwargs)

    def misdn(self, url, **kwargs):
        return self.request(AGIMethod.MISDN, url, **kwargs)

    def ustm(self, url, **kwargs):
        return self.request(AGIMethod.USTM, url, **kwargs)

    def skinny(self, url, **kwargs):
        return self.request(AGIMethod.SKINNY, url, **kwargs)

    def h323(self, url, **kwargs):
        return self.request(AGIMethod.H323, url, **kwargs)

    def ooh323(self, url, **kwargs):
        return self.request(AGIMethod.OOH323, url, **kwargs)

    def gtalk(self, url, **kwargs):
        return self.request(AGIMethod.GTALK, url, **kwargs)

    def jingle(self, url, **kwargs):
        return self.request(AGIMethod.JINGLE, url, **kwargs)

    @property
    def loop(self):
        """Session's loop."""
        return self._loop

    @property
    def closed(self):
        """Is client session closed.

        A readonly property.
        """
        return self._connector is None or self._connector.closed

    @property
    def connector(self):
        """Connector instance used for the session."""
        return self._connector

    def detach(self):
        """Detach connector from session without closing the former.

        Session is switched to closed state anyway.
        """
        self._connector = None

    async def close(self):
        """Close underlying connector.

        Release all acquired resources.
        """
        if not self.closed:
            if self._connector_owner:
                self._connector.close()
            self._connector = None
