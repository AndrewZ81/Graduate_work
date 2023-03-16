import os

from django.db import models

from core.models import User


class TgUser(models.Model):
    """
    Модель пользователя Телеграм-бота
    """
    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

    def __str__(self):
        return self.user.username

    chat_id = models.BigIntegerField(verbose_name="Chat ID Телеграм", unique=True)
    user = models.ForeignKey(
        User, verbose_name="Пользователь Web-приложения TodoList",
        on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    verification_code = models.CharField(
        max_length=30, verbose_name="Код верификации бота", null=True, blank=True, default=None
    )

    def set_verification_code(self) -> str:
        """
        Создаёт и сохраняет код верификации пользователю Телеграм
        """
        self.verification_code = os.urandom(10).hex()
        self.save(update_fields=('verification_code', ))
        return self.verification_code
