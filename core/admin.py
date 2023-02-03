from django.contrib import admin
from .models import User


@admin.register(User)  # Регистрируем и настраиваем таблицу пользователей в панели администратора
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name"]  # поля списка пользователей
    exclude = ["password"]  # не показывать пароль пользователя
    readonly_fields = ["date_joined", "last_login"]  # поля только для чтения
    search_fields = ["username", "email", "first_name", "last_name"]  # поиск по полям
    search_help_text = "Search by username, email, first_name or last_name"  # подсказка поиска
    list_filter = ["is_staff", "is_active", "is_superuser"]  # фильтр списка пользователей
