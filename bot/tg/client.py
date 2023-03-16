import requests

from accessify import private

from todolist import settings
from .schemas import GetUpdatesResponse, SendMessageResponse


class TgClient:
    """
    Описывает клиентскую часть бота
    """
    def __init__(self, token: str | None = None):
        self.token = token if token else settings.BOT_TOKEN

    @private
    def get_url(self, method: str) -> str:
        """
        Получает маршрут для обращения к боту по выбранному методу
           """
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 0) -> GetUpdatesResponse:
        """
        Получает ответ бота на команду 'getUpdates'
        """
        url = self.get_url('getUpdates')
        response = requests.get(url=url, params={'offset': offset, 'timeout': timeout}, timeout=60)
        return GetUpdatesResponse(**response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """
        Получает ответ бота на команду 'sendMessage'
        """
        url = self.get_url('sendMessage')
        response = requests.post(url=url, json={'chat_id': chat_id, 'text': text})
        return SendMessageResponse(**response.json())
