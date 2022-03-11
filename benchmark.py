import time


def bench(func):

    async def wrapper():
        start = time.time()

        await func()

        end = time.time()
        print(f'Runtime: {end - start}')

    return wrapper
