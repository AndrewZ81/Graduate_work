from django.contrib import admin

from .models import GoalCategory, Goal, GoalComment


@admin.register(GoalCategory)  # Регистрируем модель категорий с собственной панелью администратора
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created", "updated"]   # поля списка категорий
    search_fields = ["title"]  # поиск по полям
    search_help_text = "Поиск по названию"  # подсказка поиска


@admin.register(Goal)  # Регистрируем модель целей с собственной панелью администратора
class GoalAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "created", "updated"]   # поля списка целей
    search_fields = ["title", "description"]  # поиск по полям
    search_help_text = "Поиск по названию или описанию"  # подсказка поиска


@admin.register(GoalComment)  # Регистрируем модель комментариев с собственной панелью администратора
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ["text", "goal", "created", "updated"]   # поля списка комментариев
    search_fields = ["text"]  # поиск по полям
    search_help_text = "Поиск по тексту"  # подсказка поиска
