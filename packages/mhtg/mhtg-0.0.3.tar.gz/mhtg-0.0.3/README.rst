mhtg: minimal h11/trio glue
===========================

features
--------

- h11_, a transport agnostic standards-compliant http/1.1 implementation
- trio_, an async/await-native IO library focused on usability and correctness

.. _trio: https://github.com/python-trio/trio
.. _h11: https://github.com/python-hyper/h11

usage
-----

contrived example:

.. code-block:: python

   from functools import partial
   from mhtg import client, context, model
   import trio

   client_factory = partial(client.client_factory,
                            server_hostname="google.com",
                            port=443)

   connection_manager = context.make_connection_manager(client_factory)

   def request_builder():
       request = h11.Request(method="GET",
                             target="/",
                             headers=[
                                 ("host", server_hostname),
                                 ("content-length", 0),
                             ])

       return request,

   async def do():
       async with connection_manager() as reuse_connection:
           async with reuse_connection() as make_request:
               await make_request(*request_builder())

   trio.run(do)
