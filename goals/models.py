from django.db import models

from core.models import User


class DatesModelMixin(models.Model):
    """
    Базовая модель дат создания/последнего обновления объектов
    """
    class Meta:
        abstract = True  # Отключает создание таблицы БД для этой модели

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)


class Board(DatesModelMixin):
    """
    Модель общей доски целей
    """
    class Meta:
        verbose_name = "Общая доска целей"
        verbose_name_plural = "Общие доски целей"

    def __str__(self):
        return self.title

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Role(models.IntegerChoices):
    """
    Описывает набор возможных значений для поля 'role' класса 'BoardParticipant'
    """
    owner = 1, "Владелец"
    writer = 2, "Редактор"
    reader = 3, "Читатель"


class BoardParticipant(DatesModelMixin):
    """
    Модель участника общей доски целей
    """
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    board = models.ForeignKey(
        Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="participants"
    )
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="participants"
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )


class GoalCategory(DatesModelMixin):
    """
    Модель категории
    """
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

    board = models.ForeignKey(
        Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Status(models.IntegerChoices):
    """
    Описывает набор возможных значений для поля 'status' класса 'Goal'
    """
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"


class Priority(models.IntegerChoices):
    """
    Описывает набор возможных значений для поля 'priority' класса 'Goal'
    """
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(DatesModelMixin):
    """
    Модель цели
    """
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return self.title

    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    category = models.ForeignKey(
        GoalCategory, verbose_name="Категория", on_delete=models.PROTECT, related_name="goals"
    )
    due_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.PROTECT, related_name="goals"
    )
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium)


class GoalComment(DatesModelMixin):
    """
    Модель комментария цели
    """
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text

    text = models.TextField(verbose_name="Текст")
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE, related_name="comments")
