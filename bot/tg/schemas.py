from typing import List

from pydantic import BaseModel  # Используем pydantic для валидации полей классов


class Chat(BaseModel):
    """
    Описывает элемент поля 'result' ответа бота на команду 'sendMessage'
    """
    id: int


class Message(BaseModel):
    """
    Описывает поле 'result' ответа бота на команду 'sendMessage'
    """
    chat: Chat
    text: str | None = None


class UpdateObj(BaseModel):
    """
    Описывает элемент поля 'result' ответа бота на команду 'getUpdates'
    """
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    """
    Описывает ответ бота на команду 'getUpdates'
    """
    ok: bool
    result: List[UpdateObj]


class SendMessageResponse(BaseModel):
    """
    Описывает ответ бота на команду 'sendMessage'
    """
    ok: bool
    result: Message
