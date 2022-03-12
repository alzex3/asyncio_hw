from sqlalchemy import Column, Integer, String
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select

from db.database import Base, db_session


class Person(Base):
    __tablename__ = "person"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(15))
    eye_color = Column(String(15))
    films = Column(String(300))
    gender = Column(String(15))
    hair_color = Column(String(15))
    height = Column(String(15))
    homeworld = Column(String(35))
    mass = Column(String(15))
    name = Column(String(35))
    skin_color = Column(String(30))
    species = Column(String(30))
    starships = Column(String(300))
    vehicles = Column(String(300))

    @classmethod
    async def create(cls, person):
        db_session.add(person)
        await db_session.commit()

    @classmethod
    async def update(cls, person_id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == person_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db_session.execute(query)
        await db_session.commit()

    @classmethod
    async def get(cls, person_id):
        query = select(cls).where(cls.id == person_id)
        results = await db_session.execute(query)
        (result,) = results.one()
        return result
