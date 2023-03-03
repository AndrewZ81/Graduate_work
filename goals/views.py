from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination, BasePagination
from rest_framework.serializers import Serializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django.db import transaction

from .filters import GoalDateFilter
from .models import GoalCategory, Goal, Status, GoalComment, Board
from .serializers import \
    GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer, \
    BoardListSerializer
from .permissions import BoardPermissions


class BoardCreateView(generics.CreateAPIView):
    """
    Обрабатывает запрос на создание общей доски целей текущему пользователю
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = BoardCreateSerializer


class BoardListView(generics.ListAPIView):
    """
    Обрабатывает запрос на отображение списка активных общих досок целей текущего пользователя
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = BoardListSerializer
    pagination_class: BasePagination = LimitOffsetPagination

    filter_backends: list = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields: list = ["title", "created"]  # Позволяет сортировать общие доски целей по названию и дате создания
    ordering: str = "title"  # По умолчанию устанавливает сортировку по названию
    search_fields: list = ["title"]  # Позволяет искать общие доски целей по названию

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемой активной общей доски цели текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - делает неактивной (скрывает)
    """
    model = Board
    serializer_class: Serializer = BoardSerializer
    permission_classes: list = [permissions.IsAuthenticated, BoardPermissions]

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Status.archived)
        return instance


class GoalCategoryCreateView(generics.CreateAPIView):
    """
    Обрабатывает запрос на создание категории текущему пользователю
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    """
    Обрабатывает запрос на отображение списка активных категорий текущего пользователя
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = GoalCategorySerializer
    pagination_class: BasePagination = LimitOffsetPagination

    filter_backends: list = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields: list = ["title", "created"]  # Позволяет сортировать категории по названию и дате создания
    ordering: str = "title"  # По умолчанию устанавливает сортировку категорий по названию
    search_fields: list = ["title"]  # Позволяет искать категории по названию

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
    serializer_class: Serializer = GoalCategorySerializer
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
    Обрабатывает запрос на создание цели текущему пользователю
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    """
    Обрабатывает запрос на отображение списка целей текущего пользователя
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = GoalSerializer
    pagination_class: BasePagination = LimitOffsetPagination

    filter_backends: list = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class: FilterSet = GoalDateFilter
    ordering_fields: list = ["title", "created"]  # Позволяет сортировать цели по названию и дате создания
    ordering: str = "title"  # По умолчанию устанавливает сортировку по названию
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
    serializer_class: Serializer = GoalSerializer
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
    Обрабатывает запрос на создание комментария текущей цели
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    """
    Обрабатывает запрос на отображение списка комментариев текущего пользователя
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = GoalCommentSerializer
    pagination_class: BasePagination = LimitOffsetPagination

    filter_backends: list = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields: list = ["created"]  # Позволяет сортировать комментарии по дате создания
    ordering: str = "-created"  # По умолчанию устанавливает сортировку комментариев по дате создания (убывающе)
    filterset_fields: list = ["goal__title"]  # Позволяет фильтровать комментарии по названию их цели

    def get_queryset(self):
        return GoalComment.objects.filter(goal__user=self.request.user)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемого комментария текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - удаляет
    """
    serializer_class: Serializer = GoalCommentSerializer
    permission_classes: list = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__user=self.request.user)
