from sqlalchemy.exc import NoResultFound

from base.database import async_session_maker
from sqlalchemy import select, insert, delete, update


class BaseService:
    model = None

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_any(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).order_by(cls.model.id.desc())
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def insert(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def add_list_to_db(cls, data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def add_and_returning_id(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def exists(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter(*(getattr(cls.model, key) == value for key, value in filter_by.items()))
            result = await session.execute(query)
            return result.mappings().one_or_none() is not None

    @classmethod
    async def update(cls, filters: dict, **data):
        async with async_session_maker() as session:
            query_check = await cls.exists(**filters)
            if not query_check:
                raise NoResultFound(f"Not found {filters}")
            query = update(cls.model).filter_by(**filters).values(**data)
            await session.execute(query)
            await session.commit()
