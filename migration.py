import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from models import Base
from settings import PG_DSN


asyncio.set_event_loop_policy(
    asyncio.WindowsSelectorEventLoopPolicy()
)


async def async_main():
    engine = create_async_engine(PG_DSN, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(async_main())
