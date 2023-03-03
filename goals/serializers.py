from rest_framework import serializers
from django.db import transaction

from core.models import User
from core.serializers import ProfileSerializer
from .models import GoalCategory, Goal, GoalComment, Board, BoardParticipant, Role


class BoardCreateSerializer(serializers.ModelSerializer):
    """
    Создаёт общую доску целей
    """
    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"

    # Автоматически подставляет текущего пользователя в поле 'Автор'
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data) -> Board:
        user: User = validated_data.pop("user")
        board: Board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = BoardParticipant
        read_only_fields = ("id", "created", "updated", "board")
        fields = "__all__"

    role = serializers.ChoiceField(required=True, choices=Role.choices)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())


class BoardListSerializer(serializers.ModelSerializer):
    """
    Отображает список общих досок целей текущего пользователя
    """
    class Meta:
        model = Board
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    """
    Для запрашиваемой активной общей доски цели текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - делает неактивной (скрывает)
    """
    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            instance.title = validated_data["title"]
            instance.save()

        return instance


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Создаёт категорию для текущего пользователя
    """
    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "is_deleted", "user")
        fields = "__all__"

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class GoalCategorySerializer(serializers.ModelSerializer):
    """
    Отображает список категорий текущего пользователя
    Для запрашиваемой активной категории текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - делает неактивной (скрывает)
    """
    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "is_deleted", "user")
        fields = "__all__"

    user: User = ProfileSerializer(read_only=True)


class GoalCreateSerializer(serializers.ModelSerializer):
    """
    Создаёт цель для текущего пользователя
    """
    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
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
    Отображает список целей текущего пользователя
    Для запрашиваемой цели текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - архивирует (скрывает)
    """
    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Не хватает прав доступа!")
        return value


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """
    Создаёт комментарий для текущей цели
    """
    class Meta:
        model = GoalComment
        read_only_fields: tuple = ("id", "created", "updated")
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    """
    Отображает список комментариев текущего пользователя
    Для запрашиваемого комментария текущего пользователя:
    - выводит подробную информацию
    - редактирует содержимое
    - удаляет
    """
    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "goal")
        fields = "__all__"

    user: User = serializers.SerializerMethodField()

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
