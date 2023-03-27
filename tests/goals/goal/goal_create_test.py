import pytest

from goals.models import Status, Priority


@pytest.mark.django_db
def test_goal_create(client, create_new_goal):
    """
    Тестирует создание цели текущему пользователю
    """
    expected_data: dict = {
        "id": create_new_goal.data["id"],
        "category": create_new_goal.data["category"],
        "created": True,
        "updated": True,
        "title": "Тестовая цель",
        "description": None,
        "due_date": None,
        "status": Status.to_do,
        "priority": Priority.medium
    }

    received_data: dict = {
        "id": create_new_goal.data["id"],
        "category": create_new_goal.data["category"],
        "created": bool(create_new_goal.data["created"]),
        "updated": bool(create_new_goal.data["updated"]),
        "title": create_new_goal.data["title"],
        "description": create_new_goal.data["description"],
        "due_date": create_new_goal.data["due_date"],
        "status": create_new_goal.data["status"],
        "priority": create_new_goal.data["priority"],
    }

    assert all([create_new_goal.status_code == 201, received_data == expected_data])
