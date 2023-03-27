import pytest

from goals.models import Status, Priority, Role


@pytest.fixture
def get_page_not_found():
    """
    Отдаёт несуществующую страницу
    """
    return {"detail": "Страница не найдена."}


@pytest.fixture
def get_participants(create_new_user, get_board):
    """
    Отдаёт участников общей доски целей
    """
    return {
        "id": get_board.data["participants"][0]["id"],
        "role": Role.owner,
        "user": create_new_user.username,
        "created": True,
        "updated": True,
        "board": get_board.data["participants"][0]["board"]
    }


@pytest.fixture
@pytest.mark.django_db
def create_new_user(django_user_model):
    """
    Создаёт пользователя
    """
    return django_user_model.objects.create_user(
        first_name="test first name",
        last_name="test last name",
        username="pytest_user",
        password="test123qwerty",
        email="test@test.ru"
    )


@pytest.fixture
@pytest.mark.django_db
def get_profile(client, create_token):
    """
    Отдаёт профиль пользователя
    """
    return client.get(
        path="/core/profile",
        format="json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def create_token(client, create_new_user):
    """
    Создает jwt-токен
    """
    return client.post(
        path="/api/token/",
        data={"username": create_new_user.username, "password": "test123qwerty"},
        format="json"
    ).data["access"]


@pytest.fixture
@pytest.mark.django_db
def create_new_board(client, create_token):
    """
    Создаёт общую доску целей
    """
    data_for_creation: dict = {"title": "Тестовая общая доска целей"}

    return client.post(
        path="/goals/board/create",
        data=data_for_creation,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def get_board(client, create_token, create_new_board):
    """
    Получает общую доску целей по ID
    """
    return client.get(
        path=f"/goals/board/{create_new_board.data['id']}",
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def create_new_category(client, create_token, create_new_board):
    """
    Создаёт категорию текущему пользователю
    """
    data_for_creation: dict = {
        "board": create_new_board.data["id"],
        "title": "Тестовая категория"
    }

    return client.post(
        path="/goals/goal_category/create",
        data=data_for_creation,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def get_category(client, create_token, create_new_category):
    """
    Получает категорию текущего пользователя по ID
    """
    return client.get(
        path=f"/goals/goal_category/{create_new_category.data['id']}",
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def put_category(client, create_token, create_new_category):
    """
    Полностью изменяет категорию текущего пользователя по ID
    """
    return client.put(
        path=f"/goals/goal_category/{create_new_category.data['id']}",
        data={"title": "Изменённая тестовая категория"},
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def create_new_goal(client, create_token, create_new_category):
    """
    Создаёт цель текущему пользователю
    """
    data_for_creation: dict = {
        "category": create_new_category.data["id"],
        "title": "Тестовая цель"
    }

    return client.post(
        path="/goals/goal/create",
        data=data_for_creation,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def get_goal(client, create_token, create_new_goal):
    """
    Получает цель текущего пользователя по ID
    """
    return client.get(
        path=f"/goals/goal/{create_new_goal.data['id']}",
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def patch_goal(client, create_token, create_new_goal):
    """
    Частично изменяет цель текущего пользователя по ID
    """
    return client.patch(
        path=f"/goals/goal/{create_new_goal.data['id']}",
        data={
            "status": Status.done,
            "priority": Priority.high,
        },
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def create_new_comment(client, create_token, create_new_goal):
    """
    Создаёт комментарий для текущей цели
    """
    data_for_creation: dict = {
        "text": "Тестовый комментарий",
        "goal": create_new_goal.data["id"],
    }

    return client.post(
        path="/goals/goal_comment/create",
        data=data_for_creation,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def get_comment(client, create_token, create_new_comment):
    """
    Получает комментарий для текущей цели по ID
    """
    return client.get(
        path=f"/goals/goal_comment/{create_new_comment.data['id']}",
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )


@pytest.fixture
@pytest.mark.django_db
def put_comment(client, create_token, create_new_comment):
    """
    Полностью изменяет комментарий для текущей цели по ID
    """
    return client.put(
        path=f"/goals/goal_comment/{create_new_comment.data['id']}",
        data={"text": "Изменённый тестовый комментарий"},
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + create_token
    )
