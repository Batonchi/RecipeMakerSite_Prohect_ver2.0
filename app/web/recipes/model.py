from sqlalchemy import Column, Integer, String, Text, JSON
from app.base.database import Base
from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from base.database import Base


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=True)
    content = Column(JSON, default=None)

    user = relationship('User', back_populates='recipes')
