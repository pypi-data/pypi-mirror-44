########
Microbot
########

A *very* minimal class that implements the basic Telegram bot functionalities. Can (should) be extended depending on needs.

Quickstart
==========

.. code-block:: python

    import asyncio
    loop = asyncio.get_event_loop()
    bot = Bot('token')
    loop.run_until_complete(asyncio.wait([
         loop.create_task(bot.start())
         # other tasks
     ]))
     loop.run_forever()

To set the webhook you can use the ``set_webhook_url`` method.

Resources
=========
- Docs: https://strychnide.github.io/ubot/

**TODO:** documentation, testing, support sticker, inline mode, passport, payments, games, thumbnail for files, better quickstart example
