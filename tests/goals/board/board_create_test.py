import pytest


@pytest.mark.django_db
def test_board_create(create_new_board):
    """
    Тестирует создание общей доски целей
    """
    expected_data: dict = {
        "id": 1,
        "title": "Тестовая общая доска целей",

        # ЗДЕСЬ И ДАЛЕЕ
        # Ожидаем, что эти два поля просто будут получены, т.к. их значения
        # Учитывают миллисекунды, что приводит к временной разбежке между созданием и получением данных
        "created": True,
        "updated": True,

        "is_deleted": False
    }

    received_data: dict = {
        "id": create_new_board.data["id"],
        "title": create_new_board.data["title"],
        "created": bool(create_new_board.data["created"]),
        "updated": bool(create_new_board.data["updated"]),
        "is_deleted": create_new_board.data["is_deleted"]
    }

    assert all([create_new_board.status_code == 201, received_data == expected_data])
