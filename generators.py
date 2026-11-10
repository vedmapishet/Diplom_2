"""Генерация тестовых данных (фикстуры-фабрики)."""

from typing import Any, Dict, Tuple

from faker import Faker

fake = Faker()


def generate_user_data() -> Dict[str, str]:
    """Случайные данные для регистрации пользователя."""
    return {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name(),
    }


def generate_login_payload(user_data: Dict[str, str]) -> Dict[str, str]:
    """Данные для логина на основе уже созданных данных пользователя."""
    return {key: user_data[key] for key in ("email", "password")}


def generate_payloads() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Возвращает пару (payload для регистрации, payload для логина)."""
    user_data = generate_user_data()
    return user_data, generate_login_payload(user_data)
