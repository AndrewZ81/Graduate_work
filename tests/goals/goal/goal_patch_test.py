import pytest

from goals.models import Status, Priority


@pytest.mark.django_db
def test_goal_patch(client, create_new_user, patch_goal):
    """
    Тестирует частичное изменение цели текущего пользователя по ID
    """
    expected_data: dict = {
        "id": patch_goal.data["id"],
        "category": patch_goal.data["category"],
        "created": True,
        "updated": True,
        "title": "Тестовая цель",
        "description": None,
        "due_date": None,
        "status": Status.done,
        "priority": Priority.high,
        "user": create_new_user.id
    }

    received_data: dict = {
        "id": patch_goal.data["id"],
        "category": patch_goal.data["category"],
        "created": bool(patch_goal.data["created"]),
        "updated": bool(patch_goal.data["updated"]),
        "title": patch_goal.data["title"],
        "description": patch_goal.data["description"],
        "due_date": patch_goal.data["due_date"],
        "status": patch_goal.data["status"],
        "priority": patch_goal.data["priority"],
        "user": create_new_user.id
    }

    assert all([patch_goal.status_code == 200, received_data == expected_data])
