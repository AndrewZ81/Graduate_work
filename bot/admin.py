from django.contrib import admin

from .models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    """
    Модель пользователя Telegram
    """
    list_display = ["user"]
    search_fields = ["user__username"]
    search_help_text = "Поиск по логину пользователя Web-приложения TodoList"
