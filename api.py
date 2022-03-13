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
            for person_id in person_id_chunk:
                person = await asyncio.create_task(self.get_person(person_id))
                if person != {'detail': 'Not found'}:
                    person['id'] = person_id
                    yield person

    async def get_obj_name(self, obj_url):
        async with self.session.get(obj_url) as resp:
            obj = await resp.json()
            if obj.get('name'):
                return obj.get('name')
            elif obj.get('title'):
                return obj.get('title')

    async def get_objects_names(self, person, attr):
        tasks = [asyncio.create_task(self.get_obj_name(obj_url)) for obj_url in person.get(attr)]
        objs = await asyncio.gather(*tasks)
        objects_str = ', '.join(objs)
        return objects_str
