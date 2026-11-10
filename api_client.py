"""Клиент для работы с API Stellar Burgers.

Инкапсулирует все HTTP-запросы в одном месте: тестам не нужно
знать URL-адреса эндпоинтов и способ передачи токена.
"""

from typing import Any, Dict, Optional

import requests


class ApiClient:
    """Тонкая обёртка над requests для эндпоинтов Stellar Burgers."""

    BASE_URL = "https://stellarburgers.nomoreparties.site/api/"

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    # --- низкоуровневый метод ---
    def request(
        self,
        method: str,
        endpoint: str,
        token: Optional[str] = None,
        **kwargs: Any,
    ) -> requests.Response:
        headers = kwargs.pop("headers", {}) or {}
        if token:
            headers["Authorization"] = token
        return requests.request(method, self.base_url + endpoint,
                                headers=headers, **kwargs)

    # --- пользователь ---
    def register_user(self, user_data: Dict[str, Any]) -> requests.Response:
        return self.request("POST", "auth/register", json=user_data)

    def login_user(self, credentials: Dict[str, Any]) -> requests.Response:
        return self.request("POST", "auth/login", json=credentials)

    def get_user(self, token: str) -> requests.Response:
        return self.request("GET", "auth/user", token=token)

    def update_user(self, data: Dict[str, Any],
                    token: Optional[str] = None) -> requests.Response:
        return self.request("PATCH", "auth/user", token=token, json=data)

    def delete_user(self, token: str) -> requests.Response:
        return self.request("DELETE", "auth/user", token=token)

    # --- заказы ---
    def create_order(self, order_data: Dict[str, Any],
                     token: Optional[str] = None) -> requests.Response:
        return self.request("POST", "orders", token=token, json=order_data)

    def get_orders(self, token: Optional[str] = None) -> requests.Response:
        return self.request("GET", "orders", token=token)
