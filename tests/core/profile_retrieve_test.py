import pytest


@pytest.mark.django_db
def test_profile_retrieve(client, get_profile):
    """
    Тестирует получение профиля текущего пользователя
    """
    expected_data: dict = {
        "id": get_profile.data["id"],
        "first_name": "test first name",
        "last_name": "test last name",
        "email": "test@test.ru",
        "username": "pytest_user"
    }

    received_data: dict = {
        "id": get_profile.data["id"],
        "first_name": get_profile.data["first_name"],
        "last_name": get_profile.data["last_name"],
        "email": get_profile.data["email"],
        "username": get_profile.data["username"]
    }

    assert all([get_profile.status_code == 200, received_data == expected_data])
