import asyncio
import platform

from aiohttp.client import ClientSession

from benchmark import bench
from api import StarWarsAPI
from db.database import db_session
from db.models import Person


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )


@bench
async def swapi_backup():
    async with ClientSession() as aiohttp_session:

        api = StarWarsAPI(aiohttp_session)

        await db_session.init()

        async for person in api.get_persons(range(10, 15)):

            resp_person = Person(
                id=person.get('id'),
                birth_year=person.get('birth_year'),
                eye_color=person.get('eye_color'),
                films=await api.get_objects_names(person, 'films'),
                gender=person.get('gender'),
                hair_color=person.get('hair_color'),
                height=person.get('height'),
                homeworld=await api.get_obj_name(person.get('homeworld')),
                mass=person.get('mass'),
                name=person.get('name'),
                skin_color=person.get('skin_color'),
                species=await api.get_objects_names(person, 'species'),
                starships=await api.get_objects_names(person, 'starships'),
                vehicles=await api.get_objects_names(person, 'vehicles'),
            )

            await Person.update(person.get('id'), birth_year=person.get('birth_year'))
