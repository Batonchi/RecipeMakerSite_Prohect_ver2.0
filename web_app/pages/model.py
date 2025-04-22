from base.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Pages(Base):
    __tablename__ = 'pages'

    page_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, default='')
    information = Column(JSON, default=None)


class Images(Base):
    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, default='')
