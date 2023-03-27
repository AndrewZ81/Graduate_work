def test_main_page(client):
    """
    Тестирует главную страницу
    """
    response = client.get('/')
    assert response.status_code == 404

