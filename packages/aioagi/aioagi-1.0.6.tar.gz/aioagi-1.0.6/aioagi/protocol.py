import asyncio

from aiohttp import DataQueue
from aiohttp.web_protocol import RequestHandler

from aioagi.log import agi_server_logger, agi_access_logger
from aioagi.parser import AGIRequestParser, AGIPayloadParser
from aioagi.helpers import AGIAccessLogger
from aioagi.response import AGIResponse
from aioagi.agi_writer import AGIPayloadWriter
from aioagi.exceptions import AGIException, AGIInternalServerError, AGIUnprocessableEntityError


class AGIRequestHandler(RequestHandler):
    def __init__(self, *args,
                 **kwargs):
        kwargs.update(
            logger=agi_server_logger,
            access_log_class=AGIAccessLogger,
            access_log=agi_access_logger,
            access_log_format=AGIAccessLogger.LOG_FORMAT,
        )
        super().__init__(*args, **kwargs)

        self._tcp_keepalive = False
        self._messages = asyncio.Queue(1)
        self._request_parser = AGIRequestParser(self, self._loop)
        self._stream_reader = None
        self._stream_writer = None

    def connection_made(self, transport):
        super(AGIRequestHandler, self).connection_made(transport)

        self._stream_reader = DataQueue(loop=self._loop)
        self._stream_writer = AGIPayloadWriter(self, loop=self._loop)

    def data_received(self, data):
        agi_server_logger.debug(data)
        if self._force_close or self._close:
            return

        # parse agi messages
        if self._payload_parser is None:
            try:
                message = self._request_parser.feed_data(data)
            except Exception as exc:
                self.log_exception('Request parser exception', exc_info=exc)
            else:
                if message:
                    self._payload_parser = AGIPayloadParser(self._stream_reader)
                    self._messages.put_nowait(message)

        # feed payload
        elif data:
            try:
                data = self._payload_parser.feed_data(data)
                eof, tail = data
                if eof:
                    self.force_close()

            except Exception as exc:
                self.log_exception('Payload parser exception', exc_info=exc)
                self.force_close()

    async def start(self):
        message = await self._messages.get()
        request = self._request_factory(message, self, self._stream_reader, self._stream_writer, self._task_handler)

        now = self._loop.time()
        try:
            response = await self._request_handler(request)

        except AGIInternalServerError as exc:
            response = exc
            self.logger.error('AGIException', exc_info=exc)

        except AGIException as exc:
            response = exc
            self.logger.debug('AGIException', exc_info=exc)

        except asyncio.CancelledError:
            self.logger.debug('Ignored premature client disconnection')
            self.log_access(request, AGIUnprocessableEntityError(), self._loop.time() - now)
            if self.transport:
                self.transport.write(b'HANGUP\n')
            return

        except Exception as exc:
            self.logger.error('Unhandled exception', exc_info=exc)
            response = AGIInternalServerError()

        if not response:
            response = AGIResponse()

        if self.transport and response.message:
            try:
                self.transport.write('VERBOSE "{message}" {verbose}\n'.format(
                    message=response.message,
                    verbose=response.verbose,
                ).encode())

            except Exception as exc:
                self.logger.warning('Message send error', exc_info=exc)

        if self.transport and response.body:
            self.transport.write(response.body)

        self.log_access(request, response, self._loop.time() - now)
        if not self._force_close:
            if self.transport is not None:
                self.transport.close()
