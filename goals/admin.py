from django.contrib import admin

from .models import GoalCategory


@admin.register(GoalCategory)  # Регистрируем модель категорий с собственной панелью администратора
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created", "updated"]   # поля списка категорий
    search_fields = ["title", "user"]  # поиск по полям
