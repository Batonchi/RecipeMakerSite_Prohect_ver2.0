from app.base.service import BaseService
from app.web.recipes.model import Recipe
from app.base.database import async_session_maker
from sqlalchemy import insert


class RecipeService(BaseService):
    model = Recipe

    @classmethod
    async def add_recipe(cls, **data):
        """Асинхронный метод для добавления нового рецепта в базу данных."""
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()
