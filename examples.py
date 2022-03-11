import aiohttp
import asyncio
import time
import requests


async def main():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        for i in range(1, 100):
            url = f'https://swapi.dev/api/people/{i}/'
            async with session.get(url) as resp:
                print(await resp.json())
    finish = time.time()
    result = finish - start
    print(result)

asyncio.run(main())


def second():
    start = time.time()
    for i in range(1, 100):
        resp = requests.get(f'https://swapi.dev/api/people/{i}/')
        print(resp.json())
    finish = time.time()
    result = finish - start
    print(result)


second()
