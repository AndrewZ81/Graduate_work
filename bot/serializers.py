from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    """
    Верифицирует пользователя Телеграм-бота
    """
    class Meta:
        model = TgUser
        read_only_fields = ("tg_id", "user_id")
        fields = ("tg_id", "verification_code", "user_id")

    tg_id = serializers.SlugField(source='chat_id', read_only=True)

    def validate_verification_code(self, code: str):
        """
        Проверяет код верификации
        """
        try:
            self.tg_user = TgUser.objects.get(verification_code=code)
        except TgUser.DoesNotExist:
            raise ValidationError("Вы ввели неверный код верификации бота!")

        return code

    def update(self, instance: TgUser, validated_data: dict):
        """
        Возвращает пользователя Telegram без обновления его полей
        """
        return self.tg_user