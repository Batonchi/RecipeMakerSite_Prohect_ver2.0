from app.base.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Pages(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, default='')
    information = Column(JSON, default=None)


class Images(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, default='')


class Texts(Base):
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(JSON, default='')



