########
Microbot
########

A *very* minimal class that implements the basic Telegram bot functionalities. Can (should) be extended depending on needs.

Quickstart
==========

.. code-block:: python

    import asyncio
    loop = asyncio.new_event_loop()
    bot = Bot('token')
    loop.run_until_complete(asyncio.gather[
         bot.start(),
         # other tasks
         loop=loop
     ])

Resources
=========
- Docs: https://strychnide.github.io/ubot/

**TODO:** documentation, unit tests, support sticker, inline mode, passport, payments, games


