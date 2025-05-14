from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.web.users.model import User
from app.base.service import BaseService


class UserService(BaseService):
    model = User

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filter_by):
        """Асинхронно получает одного пользователя или None"""
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def insert(cls, session: AsyncSession, **data):
        """Асинхронно создает нового пользователя"""
        new_user = cls.model(**data)
        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)
        return new_user

    @classmethod
    async def update(cls, session: AsyncSession, user_id: int, **data):
        """Асинхронно обновляет данные пользователя"""
        user = await cls.get_one_or_none(session, id=user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            await session.commit()
        return user

    @classmethod
    async def delete(cls, session: AsyncSession, user_id: int):
        """Асинхронно удаляет пользователя"""
        user = await cls.get_one_or_none(session, id=user_id)
        if user:
            await session.delete(user)
