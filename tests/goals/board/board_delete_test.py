import pytest


@pytest.mark.django_db
def test_board_delete(client, create_token, create_new_board, get_page_not_found):
    """
    Тестирует удаление общей доски целей по ID
    """
    status_code: int = client.delete(
        path=f"/goals/board/{create_new_board.data['id']}",
        HTTP_AUTHORIZATION="Bearer " + create_token
    ).status_code

    received_data: dict = client.get(
        path=f"/goals/board/{create_new_board.data['id']}",
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    ).data

    assert all([status_code == 204, received_data == get_page_not_found])
