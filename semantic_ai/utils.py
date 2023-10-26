import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor


async def sync_to_async(func, *args, **kwargs):
    """
    Utility function to convert sync function to async

    :param func: Valid callable
    :param args: Input for callable arguments
    :param kwargs: Input for callable keyword arguments
    :return: Returns based on the callable
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, functools.partial(func, *args, **kwargs))


async def iter_to_aiter(iterable):
    """
    Utility function to convert sync iteration to async

    :param iterable:
    """
    for item in iterable:
        yield item
