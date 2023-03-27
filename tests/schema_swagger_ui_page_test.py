def test_schema_swagger_ui_page(client):
    """
    Тестирует страницу получения схемы Swagger-ui
    """
    response = client.get('/core/schema/swagger-ui/')
    assert response.status_code == 200
