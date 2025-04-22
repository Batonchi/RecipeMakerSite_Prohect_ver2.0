from base.database import Base
from sqlalchemy import Integer, String, Boolean, Column, JSON


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
