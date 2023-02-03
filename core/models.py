from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Переопределяем стандартную модель пользователя
    """
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
