from django.contrib import admin

from .models import GoalCategory, Goal, GoalComment, Board


# Регистрируем модели с собственными панелями администратора
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Модель общей доски целей
    """
    list_display = ["title", "created", "updated"]
    search_fields = ["title"]
    search_help_text = "Поиск по названию общей доски целей"


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    """
    Модель категорий
    """
    list_display = ["title", "user", "created", "updated"]
    search_fields = ["title"]
    search_help_text = "Поиск по названию категории"


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    """
    Модель цели
    """
    list_display = ["title", "description", "created", "updated"]
    search_fields = ["title", "description"]
    search_help_text = "Поиск по названию/описанию цели"


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    """
    Модель комментария цели
    """
    list_display = ["text", "goal", "created", "updated"]
    search_fields = ["text"]
    search_help_text = "Поиск по тексту комментария цели"
