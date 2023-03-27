import pytest


@pytest.mark.django_db
def test_category_retrieve(client, get_profile, get_category):
    """
    Тестирует получение категории текущего пользователя по ID
    """
    expected_data: dict = {
        "id": get_category.data["id"],
        "user": get_profile.data,
        "created": True,
        "updated": True,
        "title": "Тестовая категория",
        "is_deleted": False,
        "board": get_category.data["board"]
    }

    received_data: dict = {
        "id": get_category.data["id"],
        "user": get_category.data["user"],
        "created": bool(get_category.data["created"]),
        "updated": bool(get_category.data["updated"]),
        "title": get_category.data["title"],
        "is_deleted": get_category.data["is_deleted"],
        "board": get_category.data["board"],
    }

    assert all([get_category.status_code == 200, received_data == expected_data])
