from app.bots.service import AIService
from app.bots.model import AIModelProvider, YandexGPTClient, AIRequest
from app.base.constant import YANDEX_API_KEY, YANDEX_FOLDER_ID

if __name__ == "__main__":
    ai_service = AIService()

    # Регистрация клиентов
    ai_service.register_client(
        AIModelProvider.YANDEX,
        YandexGPTClient(api_key=YANDEX_API_KEY, folder_id=YANDEX_FOLDER_ID)
    )

    # Запрос к Yandex GPT
    yandex_request = AIRequest(
        prompt="Расскажи о возможностях Yandex GPT",
        model="general",
        temperature=0.5
    )
    yandex_response = ai_service.process_request(yandex_request, provider=AIModelProvider.YANDEX)
    print(yandex_response)
