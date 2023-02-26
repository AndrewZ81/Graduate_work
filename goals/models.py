from django.db import models

from core.models import User


class DatesModelMixin(models.Model):
    """
    Создаёт базовую модель для сохранения дат создания/последнего обновления объектов
    """
    class Meta:
        abstract = True  # Помечаем класс как абстрактный – для него не будет таблички в БД

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)


class GoalCategory(DatesModelMixin):
    """
    Создаёт модель для категорий
    """
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.title

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Status(models.IntegerChoices):
    """
    Создаёт набор возможных значений для поля 'status' класса 'Goal'
    """
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"


class Priority(models.IntegerChoices):
    """
    Создаёт набор возможных значений для поля 'priority' класса 'Goal'
    """
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(DatesModelMixin):
    """
    Создаёт модель для целей
    """
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self) -> str:
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
    Создаёт комментарий для цели
    """
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self) -> str:
        return self.text

    text = models.TextField(verbose_name="Текст")
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE, related_name="comments")
