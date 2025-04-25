import datetime
from base.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Boolean, Column, DateTime, ForeignKey


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
    is_admin = Column(Boolean, default=False)

    usertokens = relationship('UserToken', back_populates='user')


class UserToken(Base):
    __tablename__ = 'usertokens'

    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, nullable=True, primary_key=True)

    user = relationship('User', back_populates='usertokens')


