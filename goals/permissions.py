from rest_framework import permissions

from .models import BoardParticipant, Role


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:  # если пользователь не авторизован
            return False
        if request.method in permissions.SAFE_METHODS:  # если запрос на чтение
            return BoardParticipant.objects.filter(  # cуществует-ли участник у данной доски
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(  # если запрос на запись
            user=request.user, board=obj, role=Role.owner  # является ли текущий пользователь создателем доски
        ).exists()
