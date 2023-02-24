from rest_framework import serializers

from core.serializers import ProfileSerializer
from .models import GoalCategory


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Создаёт новую категорию для текущего пользователя
    """

    # Автоматически подставляет текущего пользователя в поле 'Автор'
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields: tuple = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")