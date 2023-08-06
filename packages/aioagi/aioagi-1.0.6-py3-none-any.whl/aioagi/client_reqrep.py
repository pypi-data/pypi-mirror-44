import sys
import attr
import asyncio
import traceback

from multidict import MultiDict

from yarl import URL
from aiohttp.helpers import CeilTimeout
from aiohttp.streams import FlowControlDataQueue, EofStream
from aiohttp.connector import Connection
from aiohttp.client_reqrep import RequestInfo

from aioagi.log import agi_client_logger
from aioagi.hdrs import AGIMethod
from aioagi.parser import AGIClientPayloadParser, AGIMessage
from aioagi.agi_writer import AGIPayloadWriter
from aioagi.client_exceptions import AGIServerTimeoutError


@attr.s(slots=True, frozen=True)
class ConnectionKey:
    # the key should contain an information about used proxy / TLS
    # to prevent reusing wrong connections from a pool
    host = attr.ib(type=str)
    port = attr.ib(type=int)
    is_ssl = attr.ib(type=bool)
    ssl = attr.ib()  # SSLContext or None
    proxy = attr.ib()  # URL or None
    proxy_auth = attr.ib()  # BasicAuth
    proxy_headers_hash = attr.ib(type=int)  # hash(CIMultiDict)


class AGIClientRequest:
    def __init__(self, method: AGIMethod, url: URL, *,
                 params=None, headers=None,
                 timeout=None, response_class=None,
                 session=None, loop=None):

        if loop is None:
            loop = asyncio.get_event_loop()

        assert isinstance(url, URL), url
        self._session = session
        self._connector = session.connector

        if params:
            q = MultiDict(url.query)
            url2 = url.with_query(params)
            q.extend(url2.query)
            url = url.with_query(q)
        self.url = url.with_fragment(None)

        self.original_url = url
        self.method = method
        self.loop = loop
        self.length = None
        self.timeout = timeout
        self.response_class = response_class or AGIClientResponse

        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

        self.ssl = False
        self.proxy = False

        self.headers = headers or {}
        self.set_headers()

        self._protocol = None
        self._connection = None
        self._writer = None
        self._reader = None
        self._response = None

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._response.close()

    @property
    def connection_key(self):
        return ConnectionKey(self.host, self.port, self.ssl, self.ssl, None, None, None)

    @property
    def host(self):
        return self.url.host

    @property
    def port(self):
        return self.url.port

    @property
    def request_info(self):
        return RequestInfo(self.url, self.method, self.headers)

    def is_ssl(self):
        return False

    def set_headers(self):
        """
        headers = {
            'agi_network': 'yes',
            'agi_network_script': 'agi/test/?a=asdf&b=jkl',
            'agi_request': 'agi://10.197.101.150:8082/agi/test/?a=asdf&b=jkl',
            'agi_channel': 'SIP/95000-00000005',
            'agi_language': 'ru',
            'agi_type': 'SIP',
            'agi_uniqueid': '1502266948.5',
            'agi_version': '11.14.2',
            'agi_callerid': '95000',
            'agi_calleridname': 'test',
            'agi_callingpres': '0',
            'agi_callingani2': '0',
            'agi_callington': '0',
            'agi_callingtns': '0',
            'agi_dnid': '770',
            'agi_rdnis': 'unknown',
            'agi_context': 'from-internal',
            'agi_extension': '770',
            'agi_priority': '2',
            'agi_enhanced': '0.0',
            'agi_accountcode': '',
            'agi_threadid': '139689736754944',
        }
        """
        self.headers['agi_type'] = self.method
        self.headers['agi_request'] = str(self.url)
        self.headers['agi_network'] = 'yes'
        self.headers['agi_network_script'] = self.url.path_qs[1:]

    async def start(self):
        # connection timeout
        try:
            with CeilTimeout(self.timeout.connect, loop=self.loop):
                connection = await self._connector.connect(self, None, self.timeout)

        except asyncio.TimeoutError as exc:
            raise AGIServerTimeoutError(
                'Connection timeout '
                'to host {0}'.format(self.url)) from exc
        else:
            self._protocol = connection.protocol
            self._connection = connection

        # connection.writer.set_tcp_nodelay(True)
        try:
            self._response = await self.send(connection)
        except Exception as exc:
            agi_client_logger.error('Request error:', exc_info=exc)
            await connection.close()
            raise

        return self._response

    async def send(self, connection: Connection):
        self._protocol = connection.protocol
        self._connection = connection

        self._writer = AGIPayloadWriter(connection.protocol, loop=self.loop)
        self._reader = FlowControlDataQueue(connection.protocol, loop=self.loop)

        connection.protocol.set_parser(AGIClientPayloadParser(self._reader), self._reader)

        # headers
        await self._writer.write_headers(self.headers)
        await self._writer.drain()

        self.response = self.response_class(
            self.method, self.original_url, connection,
            writer=self._writer, reader=self._reader,
            request_info=self.request_info,
            loop=self.loop,
        )

        return self.response


class AGIClientResponse:
    def __init__(self, method: AGIMethod, url: URL, connection: Connection,
                 writer: AGIPayloadWriter, reader: FlowControlDataQueue,
                 request_info, loop):

        self._method = method
        self._url = url
        self._connection = connection
        self._protocol = connection.protocol
        self._closed = False
        self._writer = writer
        self._reader = reader
        self._request_info = request_info
        self._waiting = None
        self._loop = loop
        self._exception = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        msg = await self.receive()
        if not msg:
            raise StopAsyncIteration()

        return msg

    @property
    def closed(self):
        return self._closed

    async def close(self):
        if self._waiting is not None and not self._closed:
            self._reader.feed_eof()
            await self._waiting

        if not self._closed:
            self._closed = True
            if self._loop is None or self._loop.is_closed():
                return

            if self._connection is not None:
                self._connection.close()
                self._connection = None

        else:
            return False

    async def send(self, message: AGIMessage):
        await self._writer.write(message.as_data())

    async def send_str(self, data):
        await self._writer.write(data)

    async def receive(self):
        if self._closed:
            return None

        self._waiting = self._loop.create_future()
        try:
            msg = await self._reader.read()
        except EofStream:
            return None
        except (asyncio.CancelledError, asyncio.TimeoutError):
            raise
        except Exception as exc:
            self._exception = exc
            agi_client_logger.exception('Message read error.', exc_info=exc)
            raise

        finally:
            waiter = self._waiting
            self._waiting = None
            waiter.set_result(True)

        return msg
