from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, ForeignKey
from app.base.database import Base
from abc import ABC, abstractmethod
from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class AIResponseData(Base):
    __tablename__ = 'ai_data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    parsed_data = Column(JSON)
    send_at = Column(DateTime, default=datetime.now())
    raw_response = Column(JSON)
    status = Column(Boolean, default=False)
    error_message = Column(String)
    handle_model = Column(String, nullable=False)

    def parse_response(self):
        pass


class AIModelProvider(Enum):
    YANDEX = "yandex"
    GIGACHAT = "gigachat"


class AIRequest(BaseModel):
    prompt: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    system_message: Optional[str] = None
    user_id: Optional[str] = None


class AIResponse(BaseModel):
    success: bool
    content: str
    model: str
    provider: AIModelProvider
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None
    raw_response: Optional[Dict] = None
    error: Optional[str] = None


class BaseAIClient(ABC):
    @abstractmethod
    def make_request(self, request: AIRequest) -> AIResponse:
        pass


