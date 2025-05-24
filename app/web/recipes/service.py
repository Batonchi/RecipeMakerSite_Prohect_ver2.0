from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.base.service import BaseService
from app.web.recipes.model import Recipe
from app.base.database import async_session_maker
from sqlalchemy import insert
from app.base.service import BaseService
from app.base.database import async_session_maker
from sqlalchemy import insert, select
import asyncio
import logging

logging.basicConfig(level=logging.INFO, filename="py_log_db.log", filemode="w")
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class RecipeService(BaseService):
    model = Recipe

    @classmethod
    async def add_recipe(cls, **data):
        async with async_session_maker() as session:
            try:
                # Проверяем соединение с БД
                await session.execute(select(1))
                # Используем прямой INSERT с RETURNING
                stmt = insert(Recipe).values(
                    user_id=data.get('user_id'),
                    name=data.get('name'),
                    content=data.get('content')
                ).returning(Recipe.id)
                result = await session.execute(stmt)
                recipe_id = result.scalar_one()
                await session.commit()
                return recipe_id

            except Exception as e:
                await session.rollback()
                current_app.logger.error(f"Database error: {str(e)}")
                return False

    @classmethod
    async def get_one_or_none(cls, **filters):
        """Асинхронное получение рецепта"""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().one_or_none()
