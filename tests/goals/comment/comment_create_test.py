import pytest


@pytest.mark.django_db
def test_comment_create(client, create_new_comment):
    """
    Тестирует создание комментария для текущей цели
    """
    expected_data: dict = {
        "id": 1,
        "text": "Тестовый комментарий",
        "goal": 1
    }

    received_data: dict = {
        "id": create_new_comment.data["id"],
        "text": create_new_comment.data["text"],
        "goal": create_new_comment.data["goal"]
    }

    assert all([create_new_comment.status_code == 201, received_data == expected_data])
