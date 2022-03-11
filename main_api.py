from aiohttp.client import ClientSession
import asyncio
from pprint import pprint
from benchmark import bench

from api import StarWarsAPI
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class APIDownloader:
    def __init__(self, new_session):
        self.session = new_session
        self.api = StarWarsAPI(self.session)

    async def result_persons(self):
        async for person in self.api.get_persons(range(1, 80)):
            pprint(person)


@bench
async def main():
    async with ClientSession() as new_session:
        new = APIDownloader(new_session)
        await new.result_persons()

asyncio.run(main())
