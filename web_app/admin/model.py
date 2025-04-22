import sqlalchemy
from sqlalchemy import orm
from base.database import Base


class Admin(Base):
    __tablename__ = 'admins'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    token = sqlalchemy.Column(sqlalchemy.String, nullable=True, primary_key=True)

    user = orm.relationship('User', back_populates='admins')
