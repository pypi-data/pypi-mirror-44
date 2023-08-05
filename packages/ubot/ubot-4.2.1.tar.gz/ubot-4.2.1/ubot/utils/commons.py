import asyncio
import random
import string


async def await_or_call(func, *args, **kwargs):
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)


def not_implemented(func):
    def decorated():
        raise NotImplementedError
    return decorated


def random_string(size=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
