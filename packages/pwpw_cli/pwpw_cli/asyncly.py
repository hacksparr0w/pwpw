import asyncio
import functools


__all__ = (
    "asyncly",
)


def asyncly(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        return asyncio.run(function(*args, **kwargs))

    return wrapper
