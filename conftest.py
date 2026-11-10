"""Общие pytest-фикстуры для тестов Stellar Burgers API."""

import pytest

from api_client import ApiClient
from generators import generate_login_payload, generate_user_data


@pytest.fixture(scope="function")
def user_data(api_client):
    """Регистрирует пользователя, отдаёт данные/токен, удаляет пользователя после теста."""
    payload = generate_user_data()
    response = api_client.register_user(payload)
    token = response.json()["accessToken"]
    yield {
        "user_data": payload,
        "login_payload": generate_login_payload(payload),
        "token": token,
        "response": response,
    }
    api_client.delete_user(token)


@pytest.fixture(scope="session")
def api_client():
    return ApiClient()
