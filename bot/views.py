from rest_framework import generics, permissions
from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework.response import Response
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class TgUserView(generics.GenericAPIView):
    """
    Обрабатывает запрос на верификацию пользователя Телеграм-бота
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = TgUserSerializer

    def patch(self, request: Request, *args, **kwargs):
        """
        Связывает пользователя Telegram с пользователем Web-приложения TodoList
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.tg_user.user = request.user
        serializer.tg_user.save()

        TgClient().send_message(
            chat_id=serializer.tg_user.chat_id,
            text="Верификация прошла успешно!"
        )
        return Response(self.get_serializer(serializer.tg_user).data)
