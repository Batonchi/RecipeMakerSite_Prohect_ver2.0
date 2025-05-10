from typing import Tuple

from app.base.constant import AUTHORIZATION_KEY
from gigachat import GigaChat
from app.bots.model import AIResponse


class AiModelsProvider:
    easy = 'GigaChat'
    normal = 'GigaChat-Pro'
    hard = 'GigaChat-Max'


class BasePrompts:
    style_text = []
    corr_text = []
    summary_text = []


class GigaBot:

    def __init__(self):
        super().__init__()
        self.authorization_key = AUTHORIZATION_KEY
        self.client = GigaChat(credentials=self.authorization_key, model='GigaChat')

    def create_payload(self):
        pass

    def style_text_prompt(self, model: str = AiModelsProvider.easy, save_history: bool = False, payload: dict = {}):
        base_payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "Ты — опытный копирайтер. Перепиши маркетинговый текст с учетом вида текста и "
                               "выбранного стиля."
                },
                {
                    "role": "user",
                    "content": "Перепиши текст как научную статью. Текст: Благодаря новой LLM GigaChat лучше следует "
                               "инструкциям и может выполнять более сложные задания: улучшилось качество "
                               "суммаризации, рерайтинга и редактирования текстов, а ответы на вопросы стали "
                               "точнее.\nПо результатам тестов новый GigaChat уже превзошел схожие по количеству "
                               "параметров иностранные аналоги в бенчмарке MMLU.\nДостичь таких результатов "
                               "получилось за счет множества экспериментов по улучшению модели и повышению "
                               "эффективности ее обучения. В частности, команда использовала фреймворк для обучения "
                               "больших языковых моделей с возможностью шардирования весов нейросети по видеокартам, "
                               "что позволило сократить потребление памяти на них.\nВ числе первых доступ к API "
                               "новинки получат бизнес-клиенты Сбера и участники академического сообщества."
                }
            ]
        }

    def summary_prompt(self, model: str = AiModelsProvider.easy, save_history: bool = False):  # hash-tags
        base_payload = {
            "model": "GigaChat-Pro",
            "messages": [
                {
                    "role": "system",
                    "content": "Выдели 5 главных фактов и мыслей из этого текста. Сформулируй каждый факт в виде "
                               "одной строки."
                },
                {
                    "role": "user",
                    "content": "<Текст>"
                }
            ],
        }
        pass

    def remark_text_prompt(self, model: str = AiModelsProvider.easy, save_history: bool = False):
        base_payload = {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "system",
                    "content": "Перепиши текст, исправив грамматические, орфографические и пунктуационные ошибки в "
                               "тексте."
                },
                {
                    "role": "user",
                    "content": "искуственый - интилектможет исправить все ошибки в даном тексте вне зависимости от "
                               "длинны"
                },
            ],
            "temperature": 0.7
        }
        pass

    def send_payload(self, payload: dict) -> AIResponse | tuple[bool, Exception]:
        try:
            result = self.client.chat(payload)
            return AIResponse(
                success=True,
                content=result.get('choices'),
                model=payload['model'],
                token_used=result.get('usage'),
                error=result.get('error')
            )
        except Exception as e:
            return False, e
