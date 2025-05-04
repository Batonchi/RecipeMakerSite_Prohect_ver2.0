from app.bots.model import (AIResponse,
                            AIRequest, AIResponseData, BaseAIClient, AIModelProvider)
from typing import Optional, Dict, Union
from app.base.service import BaseService


class AIService:
    def __init__(self):
        self.clients: Dict[AIModelProvider] = {}
        self.default_provider = AIModelProvider.DEEPSEEK

    def set_default_provider(self, provider: AIModelProvider):
        self.default_provider = provider

    def register_client(self, provider: AIModelProvider, client: BaseAIClient):
        self.clients[provider] = client

    def process_request(
            self,
            request: Union[AIRequest, str],
            provider: Optional[AIModelProvider] = None
    ) -> AIResponse:

        if isinstance(request, str):
            request = AIRequest(prompt=request)

        provider = provider or self.default_provider
        if provider not in self.clients:
            error_msg = f"No client registered for provider: {provider.value}"
            return AIResponse(
                success=False,
                content="",
                model=request.model,
                provider=provider,
                error=error_msg
            )

        client = self.clients[provider]
        return client.make_request(request)


class SaveAiResponseService(BaseService):

    def __init__(self):
        super().__init__()
        model = AIResponseData
