import asyncio
import platform

from db.database import db_session
from db.models import Person


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )


async def create_table():
    await db_session.init()
    await db_session.create_all()


if __name__ == '__main__':
    asyncio.run(create_table())
