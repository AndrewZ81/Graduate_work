from rest_framework import serializers

from core.models import User
from core.serializers import ProfileSerializer
from .models import GoalCategory, Goal, GoalComment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Создаёт новую категорию для текущего пользователя
    """
    class Meta:
        model = GoalCategory
        read_only_fields: tuple = ("id", "created", "updated", "is_deleted", "user")
        fields = "__all__"

    # Автоматически подставляет текущего пользователя в поле 'Автор'
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class GoalCategorySerializer(serializers.ModelSerializer):
    """
    Для запрашиваемой активной категории текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - делает неактивной (скрывает)
    """
    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "is_deleted", "user")

    user = ProfileSerializer(read_only=True)


class GoalCreateSerializer(serializers.ModelSerializer):
    """
    Создаёт новую цель для текущего пользователя
    """
    class Meta:
        model = Goal
        read_only_fields: tuple = ("id", "created", "updated", "user")
        fields = "__all__"

    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Не хватает прав доступа!")
        return value


class GoalSerializer(serializers.ModelSerializer):
    """
    Для запрашиваемой цели текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - архивирует (скрывает)
    """
    class Meta:
        model = Goal
        read_only_fields: tuple = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Не хватает прав доступа!")
        return value


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """
    Создаёт новый комментарий для текущей цели
    """
    class Meta:
        model = GoalComment
        read_only_fields: tuple = ("id", "created", "updated")
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    """
    Для запрашиваемого комментария текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - удаляет
    """
    class Meta:
        model = GoalComment
        read_only_fields: tuple = ("id", "created", "updated", "goal")
        fields = "__all__"

    user = serializers.SerializerMethodField()

    def get_user(self, value: GoalComment) -> dict:
        return {
            "id": value.goal.user.id,
            "username": value.goal.user.username,
            "first_name": value.goal.user.first_name,
            "last_name": value.goal.user.last_name,
            "email": value.goal.user.email
        }

    def validate_user(self, value: GoalComment) -> GoalComment:
        if value.goal.user != self.context["request"].user:
            raise serializers.ValidationError("Не хватает прав доступа!")
        return value
