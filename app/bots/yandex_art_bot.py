from enum import Enum
import requests
from typing import Optional
from dataclasses import dataclass


class AIModelProvider(Enum):
    YANDEX = "yandex"


@dataclass
class AIImageRequest:
    prompt: str
    width: int = 1024
    height: int = 1024
    num_images: int = 1


@dataclass
class AIImageResponse:
    success: bool
    images: list[str]
    model: str
    provider: AIModelProvider
    error: Optional[str] = None
    raw_response: Optional[dict] = None


class YandexARTClient:
    def __init__(self, api_key: str, folder_id: str):
        self.api_key = api_key
        self.folder_id = folder_id
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGeneration"
        self.provider = AIModelProvider.YANDEX

    def make_request(self, request: AIImageRequest) -> AIImageResponse:
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "x-folder-id": self.folder_id,
            "Content-Type": "application/json"
        }

        payload = {
            "modelUri": f"art://{self.folder_id}/yandex-art/latest",
            "generationOptions": {
                "width": request.width,
                "height": request.height
            },
            "messages": [
                {
                    "text": request.prompt,
                    "weight": 1
                }
            ],
            "numImages": request.num_images
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
            images = [img["image"] for img in response_data.get("images", [])]

            return AIImageResponse(
                success=True,
                images=images,
                model="yandex-art",
                provider=self.provider,
                raw_response=response_data
            )

        except Exception as e:
            return AIImageResponse(
                success=False,
                images=[],
                model="yandex-art",
                provider=self.provider,
                error=f"Yandex ART error: {str(e)}"
            )