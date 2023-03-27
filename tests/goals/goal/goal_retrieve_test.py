import pytest

from goals.models import Status, Priority


@pytest.mark.django_db
def test_goal_retrieve(client, create_new_user, get_goal):
    """
    Тестирует получение цели текущего пользователя по ID
    """
    expected_data: dict = {
        "id": get_goal.data["id"],
        "category": get_goal.data["category"],
        "created": True,
        "updated": True,
        "title": "Тестовая цель",
        "description": None,
        "due_date": None,
        "status": Status.to_do,
        "priority": Priority.medium,
        "user": create_new_user.id
    }

    received_data: dict = {
        "id": get_goal.data["id"],
        "category": get_goal.data["category"],
        "created": bool(get_goal.data["created"]),
        "updated": bool(get_goal.data["updated"]),
        "title": get_goal.data["title"],
        "description": get_goal.data["description"],
        "due_date": get_goal.data["due_date"],
        "status": get_goal.data["status"],
        "priority": get_goal.data["priority"],
        "user": create_new_user.id
    }
    assert all([get_goal.status_code == 200, received_data == expected_data])
