import pytest


@pytest.mark.django_db
def test_comment_delete(client, create_token, create_new_comment, get_page_not_found):
    """
    Тестирует удаление комментария текущей цели по ID
    """
    status_code: int = client.delete(
        path=f"/goals/goal_comment/{create_new_comment.data['id']}",
        HTTP_AUTHORIZATION="Bearer " + create_token
    ).status_code

    received_data: dict = client.get(
        path=f"/goals/goal_comment/{create_new_comment.data['id']}",
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    ).data

    assert all([status_code == 204, received_data == get_page_not_found])
