from rest_framework import permissions

from .models import BoardParticipant, Role, GoalCategory, Board, Goal, GoalComment


class BoardPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Board):
        """
        Проверяет права доступа к запрашиваемой общей доске целей
        """
        _filters: dict = {  # Получаем текущих пользователя и общую доску целей
            'user': request.user, 'board': obj
        }

        if request.method not in permissions.SAFE_METHODS:  # если запрос на запись
            _filters['role'] = Role.owner  # Добавляем роль владельца

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalCategory):
        """
        Проверяет права доступа к запрашиваемой активной категории
        """
        _filters: dict = {
            'user': request.user, 'board': obj.board
        }

        if request.method not in permissions.SAFE_METHODS:
            _filters['role__in'] = [Role.owner, Role.writer]  # Добавляем роли владельца и редактора

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Goal):
        """
        Проверяет права доступа к запрашиваемой цели
        """
        _filters: dict = {
            'user': request.user, 'board': obj.category.board
        }

        if request.method not in permissions.SAFE_METHODS:
            _filters['role__in'] = [Role.owner, Role.writer]  # Добавляем роли владельца и редактора

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCommentPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalComment):
        """
        Проверяет права доступа к запрашиваемому комментарию
        """
        return request.method in permissions.SAFE_METHODS or obj.goal.user == request.user
