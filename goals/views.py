from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .filters import GoalDateFilter
from .models import GoalCategory, Goal, Status, GoalComment
from .serializers import \
    GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    """
    Создаёт новую категорию для текущего пользователя
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    """
    Выводит список активных категорий текущего пользователя
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination

    filter_backends: list = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields: list = ["title", "created"]  # Позволяет сортировать категории по названию и дате создания
    ordering: str = "title"  # По умолчанию устанавливает сортировку категорий по названию
    search_fields: dict = ["title"]  # Позволяет искать категории по названию

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемой активной категории текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - делает неактивной (скрывает)
    """
    serializer_class = GoalCategorySerializer
    permission_classes: list = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted', ))
            instance.goals.update(status=Status.archived)


class GoalCreateView(generics.CreateAPIView):
    """
    Создаёт новую цель для текущего пользователя
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    """
    Выводит список целей текущего пользователя
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination

    filter_backends: list = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields: list = ["title", "created"]  # Позволяет сортировать цели по названию и дате создания
    ordering: str = "title"  # По умолчанию устанавливает сортировку целей по названию
    search_fields: list = ["title", "description"]  # Позволяет искать цели по названию и описанию

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user, category__is_deleted=False
        ).exclude(status=Status.archived)


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемой цели текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - архивирует (скрывает)
    """
    serializer_class = GoalSerializer
    permission_classes: list = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user, category__is_deleted=False
        ).exclude(status=Status.archived)

    def perform_destroy(self, instance: Goal):
        instance.status = Status.archived
        instance.save(update_fields=('status', ))


class GoalCommentCreateView(generics.CreateAPIView):
    """
    Создаёт новый комментарий для текущей цели
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    """
    Выводит список комментариев для текущего пользователя
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination

    filter_backends: list = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields: list = ["created"]  # Позволяет сортировать комментарии по дате создания
    ordering: str = "-created"  # По умолчанию устанавливает сортировку комментариев по дате создания (убывающе)
    filterset_fields: dict = ["goal__title"]  # Позволяет фильтровать комментарии по названию их цели

    def get_queryset(self):
        return GoalComment.objects.filter(goal__user=self.request.user)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемого комментария текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - удаляет
    """
    serializer_class = GoalCommentSerializer
    permission_classes: list = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__user=self.request.user)
