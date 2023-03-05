from rest_framework import generics, permissions
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
from .permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, \
    GoalCommentPermissions


class BoardCreateView(generics.CreateAPIView):
    """
    Обрабатывает запрос на создание общей доски целей текущему пользователю
    """
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: Serializer = BoardCreateSerializer


class BoardListView(generics.ListAPIView):
    """
    Обрабатывает запрос на отображение списка общих досок целей текущего пользователя
    Поддерживает сортировку по названию
    """
    permission_classes: list = [BoardPermissions]
    serializer_class: Serializer = BoardListSerializer

    filter_backends: list = [filters.OrderingFilter]
    ordering_fields: list = ["title"]
    ordering: str = "title"

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемой активной общей доски цели текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - делает неактивной (скрывает)
    """
    serializer_class: Serializer = BoardSerializer
    permission_classes: list = [BoardPermissions]

    def get_queryset(self):
        return Board.objects.filter(is_deleted=False)

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
    permission_classes: list = [GoalCategoryPermissions]
    serializer_class: Serializer = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    """
    Обрабатывает запрос на отображение списка категорий текущего пользователя
    Поддерживает сортировку по названию и дате создания, поиск по названию и
    фильтрацию по названию общей доски целей
    """
    permission_classes: list = [GoalCategoryPermissions]
    serializer_class: Serializer = GoalCategorySerializer

    filter_backends: list = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    ordering_fields: list = ["title", "created"]
    ordering: str = "title"
    search_fields: list = ["title"]
    filterset_fields: list = ["board__title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемой активной категории текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - делает неактивной (скрывает)
    """
    serializer_class: Serializer = GoalCategorySerializer
    permission_classes: list = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted', ))
            instance.goals.update(status=Status.archived)


class GoalCreateView(generics.CreateAPIView):
    """
    Обрабатывает запрос на создание цели текущему пользователю
    """
    permission_classes: list = [GoalPermissions]
    serializer_class: Serializer = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    """
    Обрабатывает запрос на отображение списка целей текущего пользователя
    Поддерживает сортировку по названию и дате создания, поиск по названию и описанию,
    фильтрацию по категории, статусу, приоритету и дате
    """
    permission_classes: list = [GoalPermissions]
    serializer_class: Serializer = GoalSerializer

    filter_backends: list = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class: FilterSet = GoalDateFilter
    ordering_fields: list = ["title", "created"]
    ordering: str = "title"
    search_fields: list = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            category__is_deleted=False
        ).exclude(status=Status.archived)


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемой цели текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - архивирует (скрывает)
    """
    serializer_class: Serializer = GoalSerializer
    permission_classes: list = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            category__is_deleted=False
        ).exclude(status=Status.archived)

    def perform_destroy(self, instance: Goal):
        instance.status = Status.archived
        instance.save(update_fields=('status', ))


class GoalCommentCreateView(generics.CreateAPIView):
    """
    Обрабатывает запрос на создание комментария текущей цели
    """
    permission_classes: list = [GoalCommentPermissions]
    serializer_class: Serializer = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    """
    Обрабатывает запрос на отображение списка комментариев текущего пользователя
    Поддерживает сортировку по дате создания и фильтрацию по названию цели
    """
    permission_classes: list = [GoalCommentPermissions]
    serializer_class: Serializer = GoalCommentSerializer

    filter_backends: list = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields: list = ["created"]
    ordering: str = "-created"
    filterset_fields: list = ["goal__title"]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемого комментария текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - удаляет
    """
    serializer_class: Serializer = GoalCommentSerializer
    permission_classes: list = [GoalCommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__user=self.request.user)
