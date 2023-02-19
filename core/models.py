from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Переопределяет стандартную модель пользователя
    """
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
