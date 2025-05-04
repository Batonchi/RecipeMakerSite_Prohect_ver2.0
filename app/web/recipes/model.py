from sqlalchemy import Column, Integer, String, Text, JSON
from app.base.database import Base


class Recipe(Base):
    __tablename__ = 'recipes'

    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    name_recipe = Column(String, nullable=True)
    description = Column(Text, nullable=False, default='')
    look = Column(JSON, default=None)
