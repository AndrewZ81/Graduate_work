import pytest

from django.http import response


@pytest.mark.django_db
def test_token_obtain_pair(client, create_token, create_new_user):
    """
    Тестирует получение jwt-токенов
    """
    expected_data: dict = {  # Ожидаем, что токены просто будут получены,
        "refresh": True,     # Т.к. их значения постоянно меняются
        "access": True
    }

    _response: response = client.post(
        path="/api/token/",
        data={"username": create_new_user.username, "password": "test123qwerty"},
        format="json"
    )

    received_data: dict = {
        "refresh": bool(_response.data["refresh"]),  # Если токены будут получены,
        "access": bool(_response.data["access"]),    # Они примут значения True
    }

    assert all([_response.status_code == 200, received_data == expected_data])
