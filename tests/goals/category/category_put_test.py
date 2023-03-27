import pytest


@pytest.mark.django_db
def test_category_put(client, get_profile, put_category):
    """
    Тестирует полное изменение категории текущего пользователя по ID
    """
    expected_data: dict = {
        "id": put_category.data["id"],
        "user": get_profile.data,
        "created": True,
        "updated": True,
        "title": "Изменённая тестовая категория",
        "is_deleted": False,
        "board": put_category.data["board"]
    }

    received_data: dict = {
        "id": put_category.data["id"],
        "user": put_category.data["user"],
        "created": bool(put_category.data["created"]),
        "updated": bool(put_category.data["updated"]),
        "title": put_category.data["title"],
        "is_deleted": put_category.data["is_deleted"],
        "board": put_category.data["board"],
    }

    assert all([put_category.status_code == 200, received_data == expected_data])
