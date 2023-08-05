import asyncio
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .utils import await_or_call


class Bot:
    update_types = [
        ('message', 'message'),
        ('edited_message', 'message'),
        ('channel_post', 'message'),
        ('edited_channel_post', 'message'),
        ('inline_query', 'inline_query'),
        ('chosen_inline_result', 'chosen_inline_result'),
        ('callback_query', 'callback_query'),
        ('shipping_query', 'shipping_query'),
        ('pre_checkout_query', 'pre_checkout_query')
    ]

    # optional methods
    check_update = None

    def __init__(self, token, loop=None):
        """
        The Class(TM).

        :param token: The Telegram-given token
        :param max_triggers: The max number of triggers to execute for a single update
        :param loop: The loop the bot is run into (if it's not asyncio.get_event_loop())
        """

        self.token = token

        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.triggers = []
        self.ignore_check_triggers = []
        self.update_queue = asyncio.PriorityQueue(loop=self.loop)
        self.base_url = 'https://api.telegram.org:443/bot%s/' % token

    async def __api_request(self, method, endpoint, args=None, data=None, headers=None):
        """
        Wraps the urllib3 request in a more user friendly way, making it async and premitting the base Telegram API url.

        :param method: The HTTP method name (GET, POST, PUT, DELETE, HEAD)
        :param endpoint: A Telegram API endpoint (e.g. sendMessage), omitting
            the first slash
        :param args: The get string arguments
        :param data: Binary data to be sent with the request
        :param headers: A CaseInsensitiveDict of headers
        :return: The response from the server
        """

        if args:
            url = f'{self.base_url}{endpoint}?{urlencode(args)}'
        else:
            url = f'{self.base_url}{endpoint}'

        if data and 'content-length' not in headers:
            headers['content-length'] = len(data)

        req = Request(url=url, method=method, data=data, headers=headers)
        res = await self.loop.run_in_executor(None, urlopen, req)
        return res

    async def start(self):
        """
        Main loop

        >>> import asyncio
        >>> loop = asyncio.get_event_loop()
        >>> bot = Bot('token')
        >>> loop.run_until_complete(asyncio.wait([
        >>>     bot.start(),
        >>>     # other tasks
        >>> ]))
        """

        while True:
            _, update = await self.update_queue.get()
            self.loop.create_task(self.handle_update(update))

    async def handle_update(self, update):
        # get type and flavor (if they're none, it's probably an error)
        for _type, flavor in self.update_types:
            if _type in update:
                update_type, update_flavor = _type, flavor
                break
        else:
            update_type, update_flavor = None, None

        # check the update if the function is implemented and skip if it's not passed
        check_update = self.check_update
        if check_update is None:
            checked_triggers = self.triggers + self.ignore_check_triggers
        else:
            is_check_passed = await await_or_call(check_update, update, update_type, update_flavor)
            if is_check_passed is True:
                checked_triggers = self.triggers + self.ignore_check_triggers
            else:
                checked_triggers = self.triggers

        for trigger in checked_triggers:

            is_update_matched = await await_or_call(trigger.match, update, update_type, update_flavor)

            if is_update_matched is not True:
                continue

            # if a matching one is found call the corresponding handler
            endpoint = await await_or_call(trigger.handle, update, update_type, update_flavor)

            if endpoint is None:
                continue

            method, url, args, data, headers = endpoint

            response = await self.__api_request(method, url, args, data, headers)

            # call the callback if existing
            callback = trigger.callback

            if callback is not None:
                await await_or_call(callback, response)

            break

    def push_update(self, update):
        """
        Pushes an update (already json decoded) into the queue.

        :param update: The update to be pushed in the queue
        """

        self.update_queue.put_nowait((update['update_id'], update))

    def trigger(self, ignore_check=False):
        """
        Decorates a Trigger, inserting it into the bot check list

        :param ignore_check: ignores a possible "check_update" function
        """

        def decorator(trigger):
            if ignore_check is True:
                self.ignore_check_triggers.append(trigger())
            else:
                self.triggers.append(trigger())

            return trigger

        return decorator
