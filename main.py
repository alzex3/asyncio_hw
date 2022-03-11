import aiohttp
import asyncio

from tests import test_person, test_person_2
from benchmark import bench
from api import StarWarsAPI
from pprint import pprint
from models import Person, Base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from more_itertools import chunked
from database import async_db_session
from models import Person

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# async def create_person():
#     await Person.create(test_person)
#     person = await Person.get(1)
#     return person.id
#
#
# async def init_app():
#     await async_db_session.init()
#     await async_db_session.create_all()
#
#
# async def async_main():
#     await init_app()
#     person_id = await create_person()
#
#
# asyncio.run(async_main())


async def async_main():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/async_hw",
        echo=True,
    )

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [test_person, test_person_2]
            )

    # await session.commit()
    await engine.dispose()
# asyncio.run(async_main())

