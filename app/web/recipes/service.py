from app.base.service import BaseService
from app.web.recipes.model import Recipe
from app.base.database import async_session_maker
from sqlalchemy import insert
from app.base.service import BaseService
from app.base.database import async_session_maker
from sqlalchemy import insert, select
import asyncio


class RecipeService(BaseService):
    model = Recipe

    @classmethod
    async def add_recipe(cls, **data):
        """Асинхронный метод для добавления нового рецепта в базу данных."""
        async with async_session_maker() as session:
            try:
                print("Пытаемся сохранить рецепт:", data)  # Логирование
                stmt = insert(cls.model).values(**data)
                result = await session.execute(stmt)
                await session.commit()
                print("Рецепт успешно сохранён, ID:", result.inserted_primary_key)
                return True
            except Exception as e:
                await session.rollback()
                print("Ошибка при сохранении рецепта:", str(e))
                raise e

    @classmethod
    async def get_one_or_none(cls, **filters):
        """Асинхронное получение рецепта"""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().one_or_none()
