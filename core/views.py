from typing import Any
from django.contrib.auth import login, logout
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.request import Request

from .models import User
from .serializers import RegisterUserSerializer, LoginSerializer, ProfileSerializer, ChangePasswordSerializer


class RegisterUserView(generics.CreateAPIView):
    """
    Регистрирует (создаёт) нового пользователя
    """
    serializer_class = RegisterUserSerializer


class LoginView(generics.CreateAPIView):
    """
    Осуществляет аутентификацию пользователя
    """
    serializer_class = LoginSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Выводит профиль пользователя и редактирует его при необходимости.
    Осуществляет завершение сеанса пользователя
    """
    serializer_class: ProfileSerializer = ProfileSerializer
    permission_classes: tuple = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance: User):
        logout(self.request)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Осуществляет смену пароля пользователя
    """
    serializer_class: ChangePasswordSerializer = ChangePasswordSerializer
    permission_classes: tuple = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user
