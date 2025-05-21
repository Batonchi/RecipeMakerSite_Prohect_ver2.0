from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.web.users.model import User, Guest
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
    async def insert(cls, session, **data):
        try:
            user = cls.model(**data)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        except Exception as e:
            print(f"Ошибка при создании пользователя: {str(e)}")
            await session.rollback()
            raise

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


class GuestService(BaseService):
    """Здесь планируются какие-то методы"""
    model = Guest

