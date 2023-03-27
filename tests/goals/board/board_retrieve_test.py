import pytest


@pytest.mark.django_db
def test_board_retrieve(client, get_participants, get_board):
    """
    Тестирует получение общей доски целей по ID
    """
    expected_data: dict = {
        "id": get_board.data["id"],
        "participants": [get_participants],
        "created": True,
        "updated": True,
        "title": "Тестовая общая доска целей",
        "is_deleted": False
    }

    received_data: dict = {
        "id": get_board.data["id"],
        "participants": [
            {
                "id": get_board.data["participants"][0]["id"],
                "role": get_board.data["participants"][0]["role"],
                "user": get_board.data["participants"][0]["user"],
                "created": bool(get_board.data["participants"][0]["created"]),
                "updated": bool(get_board.data["participants"][0]["updated"]),
                "board": get_board.data["participants"][0]["board"]
            }
        ],
        "created": bool(get_board.data["created"]),
        "updated": bool(get_board.data["updated"]),
        "title": get_board.data["title"],
        "is_deleted": get_board.data["is_deleted"]
    }
    assert all([get_board.status_code == 200, received_data == expected_data])
