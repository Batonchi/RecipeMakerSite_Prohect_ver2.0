from app.bots.model import BaseAIClient, AIModelProvider, AIRequest, AIResponse
import requests


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