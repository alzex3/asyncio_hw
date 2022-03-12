import asyncio
import platform
from more_itertools import chunked

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )


class StarWarsAPI:
    def __init__(self, aiohttp_session):
        self.session = aiohttp_session
        self.base_url = 'https://swapi.dev/api/'

    async def get_person(self, person_id):
        url = self.base_url + 'people/' + str(person_id)
        async with self.session.get(url) as resp:
            person = await resp.json()
            return person

    async def get_persons(self, range_person_id):
        for person_id_chunk in chunked(range_person_id, 15):
            tasks = [asyncio.create_task(self.get_person(person_id)) for person_id in person_id_chunk]
            persons = await asyncio.gather(*tasks)

            for person in persons:
                if await self.is_exist(person):
                    yield person

    async def get_obj_name(self, obj_url):
        async with self.session.get(obj_url) as resp:
            obj = await resp.json()
            if obj.get('name'):
                return obj.get('name')
            elif obj.get('title'):
                return obj.get('title')
            else:
                return ''

    async def get_object(self, person, attr):
        return await self.get_obj_name(person.get(attr))

    async def get_objects_names(self, person, attr):
        tasks = [asyncio.create_task(self.get_obj_name(obj)) for obj in person.get(attr)]
        objs = await asyncio.gather(*tasks)
        objects_str = ', '.join(objs)
        return objects_str

    @staticmethod
    async def is_exist(person):
        if person != {'detail': 'Not found'}:
            return True

    # @staticmethod
    # async def has_attribute(person, attr):
    #     if person.get(attr):
    #         return True

    async def get_objs_names(self, person, attr):
        if type(person.get(attr)) == list:
            return await self.get_objects_names(person, attr)

        elif type(person.get(attr)) == str:
            return await self.get_object(person, attr)

        else:
            return ''
