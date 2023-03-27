import pytest


@pytest.mark.django_db
def test_comment_put(client, get_profile, put_comment):
    """
    Тестирует полное изменение комментария текущей цели по ID
    """
    expected_data: dict = {
        "id": put_comment.data["id"],
        "user": get_profile.data,
        "created": True,
        "updated": True,
        "text": "Изменённый тестовый комментарий",
        "goal": put_comment.data["goal"]
    }

    received_data: dict = {
        "id": put_comment.data["id"],
        "user": {
            "id": put_comment.data["user"]["id"],
            "username": put_comment.data["user"]["username"],
            "first_name": put_comment.data["user"]["first_name"],
            "last_name": put_comment.data["user"]["last_name"],
            "email": put_comment.data["user"]["email"],

        },
        "created": bool(put_comment.data["created"]),
        "updated": bool(put_comment.data["updated"]),
        "text": put_comment.data["text"],
        "goal": put_comment.data["goal"]
    }

    assert all([put_comment.status_code == 200, received_data == expected_data])
