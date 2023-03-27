def test_schema_redoc_page(client):
    """
    Тестирует страницу получения схемы Redoc
    """
    response = client.get('/core/schema/redoc/')
    assert response.status_code == 200
