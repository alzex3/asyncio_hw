import asyncio
from more_itertools import chunked
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class StarWarsAPI:
    def __init__(self, session):
        self.session = session
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
                if await self.is_person_exist(person):
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

    async def get_object(self, person, obj):
        if person.get(obj):
            return await self.get_obj_name(person.get(obj))
        else:
            return ''

    async def get_objects_names(self, person, objs):
        if person.get(objs):
            tasks = [asyncio.create_task(self.get_obj_name(obj)) for obj in person.get(objs)]
            objs = await asyncio.gather(*tasks)
            objects_str = ', '.join(objs)
            return objects_str
        else:
            return ''

    @staticmethod
    async def is_person_exist(person):
        if person != {'detail': 'Not found'}:
            return True
