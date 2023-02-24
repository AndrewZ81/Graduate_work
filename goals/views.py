from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from .models import GoalCategory
from .serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    """
    Создаёт новую категорию для текущего пользователя
    """
    model = GoalCategory
    permission_classes: tuple = (permissions.IsAuthenticated, )
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    """
    Выводит список активных категорий текущего пользователя
    """
    model = GoalCategory
    permission_classes: tuple = (permissions.IsAuthenticated, )
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]  # Позволяет сортировать категории по названию и дате создания
    ordering = ["title"]  # По умолчанию устанавливает сортировку категорий по названию
    search_fields = ["title"]  # Позволяет искать категории по названию и дате создания

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для запрашиваемой активной категории текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - делает неактивной
    """
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes: tuple = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance
