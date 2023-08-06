from aiohttp.abc import AbstractStreamWriter

from aioagi.commands import AGICommand


class AGIPayloadWriter(AbstractStreamWriter):

    def __init__(self, protocol, loop):
        self._protocol = protocol
        self._transport = protocol.transport

        self.loop = loop
        self._eof = False

    @property
    def transport(self):
        return self._transport

    @property
    def protocol(self):
        return self._protocol

    async def write(self, chunk):
        """Writes chunk of data to a stream.

        write_eof() indicates end of stream.
        writer can't be used after write_eof() method being called.
        write() return drain future.
        """
        chunk = chunk.encode('utf-8')
        if chunk:
            if self._transport is None or self._transport.is_closing():
                raise ConnectionResetError('Cannot write to closing transport')
            self._transport.write(chunk)

    async def write_headers(self, headers, SEP=': ', END='\n'):
        """Write request headers."""
        # status + headers
        headers = ''.join(
            [k + SEP + v + END for k, v in headers.items()]
        )
        headers = headers + '\n'

        await self.write(headers)

    async def write_eof(self, chunk=b''):
        if self._eof:
            return

        if not chunk:
            chunk = AGICommand.HANGUP.value.encode('utf-8')
            chunk = chunk + b'\n'

        self.write(chunk)
        await self.drain(True)

        self._eof = True
        self._transport = None

    async def drain(self, last=False):
        """Flush the write buffer.

        The intended use is to write

          await w.write(data)
          await w.drain()
        """
        if self._protocol.transport is not None:
            await self._protocol._drain_helper()
