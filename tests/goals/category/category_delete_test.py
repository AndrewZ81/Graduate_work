import pytest


@pytest.mark.django_db
def test_category_delete(client, create_token, create_new_category, get_page_not_found):
    """
    Тестирует удаление категории текущего пользователя по ID
    """
    status_code: int = client.delete(
        path=f"/goals/goal_category/{create_new_category.data['id']}",
        HTTP_AUTHORIZATION="Bearer " + create_token
    ).status_code

    received_data: dict = client.get(
        path=f"/goals/goal_category/{create_new_category.data['id']}",
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    ).data

    assert all([status_code == 204, received_data == get_page_not_found])
