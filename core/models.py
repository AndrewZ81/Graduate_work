from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Переопределяем стандартную модель пользователя
    """
    pass
