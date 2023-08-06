Aioagi
======

Async agi client/server framework.
The project based on "aiohttp" framework.

Key Features
============

- Supports both client and server side of AGI protocol.
- AGI-server has middlewares and pluggable routing.

Getting started
===============


Server
------

Simple AGI server:

.. code-block:: python

    from aioagi import runner
    from aioagi.app import AGIApplication
    from aioagi.log import agi_server_logger
    from aioagi.urldispathcer import AGIView


    async def hello(request):
        message = await request.agi.stream_file('hello-world')
        await request.agi.verbose('Hello handler: {}.'.format(request.rel_url.query))
        agi_server_logger.debug(message)


    class HelloView(AGIView):
        async def sip(self):
            message = await self.request.agi.stream_file('hello-world')
            await self.request.agi.verbose('HelloView handler: {}.'.format(self.request.rel_url.query))
            agi_server_logger.debug(message)


    if __name__ == '__main__':
        logging.config.dictConfig(LOGGING)
        app = AGIApplication()
        app.router.add_route('SIP', '/', hello)
        runner.run_app(app)

Client
------

To set AGI connection as Asterisk:

.. code-block:: python

    import asyncio
    import logging.config

    from aioagi.log import agi_client_logger
    from aioagi.client import AGIClientSession
    from aioagi.parser import AGIMessage, AGICode


    async def test_request(loop):
        headers = {
            'agi_channel': 'SIP/100-00000001',
            'agi_language': 'ru',
            'agi_uniqueid': '1532375920.8',
            'agi_version': '14.0.1',
            'agi_callerid': '100',
            'agi_calleridname': 'test',
            'agi_callingpres': '0',
            'agi_callingani2': '0',
            'agi_callington': '0',
            'agi_callingtns': '0',
            'agi_dnid': '101',
            'agi_rdnis': 'unknown',
            'agi_context': 'from-internal',
            'agi_extension': '101',
            'agi_priority': '1',
            'agi_enhanced': '0.0',
            'agi_accountcode': '',
            'agi_threadid': '139689736754944',
        }
        async with AGIClientSession(headers=headers, loop=loop) as session:
            async with session.sip('agi://localhost:8080/hello/?a=test1&b=var1') as response:
                async for message in response:
                    client_logger.debug(message)
                    await response.send(AGIMessage(AGICode.OK, '0', {}))

            async with session.sip('agi://localhost:8080/hello-view/?a=test2&b=var2') as response:
                async for message in response:
                    client_logger.debug(message)
                    await response.send(AGIMessage(AGICode.OK, '0', {}))

.. note:: Session request headers are set automatically for ``session.sip('agi://localhost:8080/hello/?a=test1&b=var1')`` request:

.. code-block::

    agi_type: SIP
    agi_network: yes
    agi_network_script: hello/
    agi_request: agi://localhost:8080/hello/


Install
=======

``pip install aioagi``
