from sqlalchemy import Column, Integer, String
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select

from database import Base, async_db_session


class ModelAdmin:
    @classmethod
    async def create(cls, *args):
        async_db_session.add(*args)
        await async_db_session.commit()

    @classmethod
    async def update(cls, person_id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == person_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, person_id):
        query = select(cls).where(cls.id == person_id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result


class Person(Base, ModelAdmin):
    __tablename__ = "person"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(4))
    eye_color = Column(String(15))
    films = Column(String(300))
    gender = Column(String(10))
    hair_color = Column(String(15))
    height = Column(String(5))
    homeworld = Column(String(35))
    mass = Column(String(5))
    name = Column(String(35))
    skin_color = Column(String(15))
    species = Column(String(15))
    starships = Column(String(300))
    vehicles = Column(String(300))
