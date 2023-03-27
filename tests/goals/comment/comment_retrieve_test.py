import pytest


@pytest.mark.django_db
def test_comment_retrieve(client, get_profile, get_comment):
    """
    Тестирует получение комментария текущей цели по ID
    """
    expected_data: dict = {
        "id": get_comment.data["id"],
        "user": get_profile.data,
        "created": True,
        "updated": True,
        "text": "Тестовый комментарий",
        "goal": get_comment.data["goal"]
    }

    received_data: dict = {
        "id": get_comment.data["id"],
        "user": {
                "id": get_comment.data["user"]["id"],
                "username": get_comment.data["user"]["username"],
                "first_name": get_comment.data["user"]["first_name"],
                "last_name": get_comment.data["user"]["last_name"],
                "email": get_comment.data["user"]["email"],

        },
        "created": bool(get_comment.data["created"]),
        "updated": bool(get_comment.data["updated"]),
        "text": get_comment.data["text"],
        "goal": get_comment.data["goal"]
    }

    assert all([get_comment.status_code == 200, received_data == expected_data])
