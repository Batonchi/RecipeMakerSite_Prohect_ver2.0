from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, ForeignKey
from base.database import Base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import json
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import requests


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
    DEEPSEEK = "deepseek"
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


class DeepSeekClient(BaseAIClient):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.provider = AIModelProvider.DEEPSEEK  # Нужно добавить этот провайдер в enum

    def make_request(self, request: AIRequest) -> AIResponse:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if request.system_message:
            messages.append({"role": "system", "content": request.system_message})
        messages.append({"role": "user", "content": request.prompt})

        payload = {
            "model": "deepseek-chat",  # Укажите актуальную модель DeepSeek
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }

        try:
            start_time = datetime.now()
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            response_data = response.json()

            processing_time = (datetime.now() - start_time).total_seconds()

            return AIResponse(
                success=True,
                content=response_data["choices"][0]["message"]["content"],
                model=request.model,
                provider=self.provider,
                tokens_used=response_data.get("usage", {}).get("total_tokens"),
                processing_time=processing_time,
                raw_response=response_data
            )

        except Exception as e:
            error_msg = f"DeepSeek request failed: {str(e)}"
            return AIResponse(
                success=False,
                content="",
                model=request.model,
                provider=self.provider,
                error=error_msg
            )


class YandexGPTClient(BaseAIClient):
    def __init__(self, api_key: str, folder_id: str):
        self.api_key = api_key
        self.folder_id = folder_id
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.provider = AIModelProvider.YANDEX

    def make_request(self, request: AIRequest) -> AIResponse:
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "x-folder-id": self.folder_id,
            "Content-Type": "application/json"
        }

        payload = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
            "completionOptions": {
                "temperature": request.temperature,
                "maxTokens": request.max_tokens
            },
            "messages": [
                {
                    "role": "user",
                    "text": request.prompt
                }
            ]
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            response_data = response.json()

            return AIResponse(
                success=True,
                content=response_data["result"]["alternatives"][0]["message"]["text"],
                model="yandexgpt-lite",
                provider=self.provider,
                raw_response=response_data
            )

        except Exception as e:
            return AIResponse(
                success=False,
                content="",
                model="yandexgpt-lite",
                provider=self.provider,
                error=f"Yandex GPT error: {str(e)}"
            )