from base.database import Base
import datetime
from sqlalchemy import Integer, String, Boolean, Column, JSON, DateTime


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    last_visit_date = Column(DateTime, default=datetime.datetime.now)
    email = Column(String, index=True, unique=True, nullable=True)
    date_of_birth = Column(DateTime)
    password = Column(String, nullable=True)
