import asyncio


def memoize_concurrent(func):

    cache = {}

    async def memoized(*args, **kwargs):
        key = (args, tuple(kwargs.items()))

        try:
            future = cache[key]
        except KeyError:
            future = asyncio.Future()
            cache[key] = future

            try:
                result = await func(*args, **kwargs)
            except BaseException as exception:
                future.set_exception(exception)
            else:
                future.set_result(result)
            finally:
                del cache[key]

        return await future

    return memoized
