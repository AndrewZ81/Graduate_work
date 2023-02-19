from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from .models import User


class PasswordField(serializers.CharField):
    """
    Переопределяет поле 'password' модели 'User' и
    добавляет дополнительную проверку на его сложность
    """
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Регистрирует (создаёт) нового пользователя
    """
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'username', 'email', 'password', 'password_repeat',
        )

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError("Пароли не совпадают!")
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """
    Осуществляет аутентификацию пользователя
    """
    username = serializers.CharField()
    password = PasswordField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')
        read_only_fields = ('id', 'first_name', 'last_name', 'email',)

    def create(self, validated_data: dict) -> User:
        if user := authenticate(
            username=validated_data['username'],
            password=validated_data['password'],
        ):
            return user
        raise AuthenticationFailed


class ProfileSerializer(serializers.ModelSerializer):
    """
    Выводит профиль пользователя и редактирует его при необходимости.
    Осуществляет завершение сеанса пользователя
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username',)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Осуществляет смену пароля пользователя
    """
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate_old_password(self, old_password: str) -> str:
        if not self.instance.check_password(old_password):
            raise ValidationError("Прежний пароль неверный!")
        return old_password

    def update(self, instance: User, validated_data: dict) -> User:
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=('password', ))
        return instance
