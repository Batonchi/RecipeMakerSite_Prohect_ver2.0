import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.base.database import Base


class Complaint(Base):
    __tablename__ = 'complaints'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String, nullable=False)
    date_pushed = Column(DateTime, default=datetime.datetime.now)
    is_solved = Column(Boolean, default=False)

    user = relationship('User', back_populates='complaints')
