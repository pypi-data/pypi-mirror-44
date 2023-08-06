import asyncio

from yarl import URL
from aiohttp.web_runner import BaseSite, AppRunner, GracefulExit


class AGISite(BaseSite):
    __slots__ = ('_host', '_port', '_reuse_address', '_reuse_port')

    def __init__(self, runner, host=None, port=None, *,
                 shutdown_timeout=60.0, ssl_context=None,
                 backlog=128, reuse_address=None,
                 reuse_port=None):
        super().__init__(runner, shutdown_timeout=shutdown_timeout,
                         ssl_context=ssl_context, backlog=backlog)
        if host is None:
            host = "0.0.0.0"
        self._host = host

        if port is None:
            port = 8080
        self._port = port

        self._reuse_address = reuse_address
        self._reuse_port = reuse_port

    @property
    def name(self):
        return str(URL.build(scheme='agi', host=self._host, port=self._port))

    async def start(self):
        await super().start()
        loop = asyncio.get_event_loop()
        self._server = await loop.create_server(
            self._runner.server, self._host, self._port,
            ssl=self._ssl_context, backlog=self._backlog,
            reuse_address=self._reuse_address,
            reuse_port=self._reuse_port)


def run_app(app, *, host=None, port=None,
            shutdown_timeout=60.0,
            print=print, backlog=128, handle_signals=True,
            reuse_address=None, reuse_port=None):

    loop = asyncio.get_event_loop()

    if asyncio.iscoroutine(app):
        app = loop.run_until_complete(app)

    runner = AppRunner(app, handle_signals=handle_signals)
    loop.run_until_complete(runner.setup())

    try:
        loop.run_until_complete(get_site(
            runner,
            host=host, port=port,
            shutdown_timeout=shutdown_timeout, backlog=backlog,
            reuse_address=reuse_address, reuse_port=reuse_port,
        ))
        try:
            if print:  # pragma: no branch
                names = sorted(str(s.name) for s in runner.sites)
                print("======== Running on {} ========\n"
                      "(Press CTRL+C to quit)".format(', '.join(names)))
            loop.run_forever()
        except (GracefulExit, KeyboardInterrupt):  # pragma: no cover
            pass
    finally:
        loop.run_until_complete(runner.cleanup())
    if hasattr(loop, 'shutdown_asyncgens'):
        loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


async def get_site(runner, *,
                   host=None, port=None,
                   shutdown_timeout=60.0, backlog=128,
                   reuse_address=None, reuse_port=None):

    site = AGISite(runner, host, port,
                   shutdown_timeout=shutdown_timeout,
                   backlog=backlog,
                   reuse_address=reuse_address,
                   reuse_port=reuse_port)

    await site.start()
