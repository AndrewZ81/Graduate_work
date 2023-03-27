import pytest

from goals.models import Board


@pytest.mark.django_db
def test_category_create(client, create_new_category):
    """
    Тестирует создание категории текущему пользователю
    """
    expected_data: dict = {
        "id": create_new_category.data["id"],
        "board": create_new_category.data["board"],
        "created": True,
        "updated": True,
        "title": "Тестовая категория",
        "is_deleted": False
    }

    received_data: dict = {
        "id": create_new_category.data["id"],
        "board": create_new_category.data["board"],
        "created": bool(create_new_category.data["created"]),
        "updated": bool(create_new_category.data["updated"]),
        "title": create_new_category.data["title"],
        "is_deleted": create_new_category.data["is_deleted"]
    }
    assert all([create_new_category.status_code == 201, received_data == expected_data])
