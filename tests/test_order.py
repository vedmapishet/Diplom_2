import allure
import pytest

from data import DataTest, ResponseBody


@pytest.fixture(scope="class")
def valid_token():
    """Токен авторизованного пользователя для тестов заказов."""
    from generators import generate_user_data
    from api_client import ApiClient

    response = ApiClient().register_user(generate_user_data())
    return response.json()["accessToken"]


class TestCreatingOrder:
    @allure.title("POST запрос - Успешное создание заказа с авторизацией")
    def test_create_order(self, api_client, user_data):
        response = api_client.create_order(
            DataTest.data_order, token=user_data["token"]
        )
        assert response.status_code == 200
        assert response.json()["success"]

    @allure.title("POST запрос - НЕуспешное создание заказа без ингредиентов")
    @pytest.mark.parametrize(
        "with_token",
        [
            pytest.param(True, id="с токеном"),
            pytest.param(False, id="без токена"),
        ],
    )
    def test_create_order_not_ingredients(self, api_client, valid_token, with_token):
        token = valid_token if with_token else None
        response = api_client.create_order(
            DataTest.data_order_not_ingredients, token=token
        )
        assert response.status_code == 400
        assert response.json() == ResponseBody.respons_body_not_ingredients

    @allure.title(
        "POST запрос - НЕуспешное создание заказа с неверным хешем ингредиентов"
    )
    def test_create_order_with_an_incorrect_hash_of_ingredients(
        self, api_client, valid_token
    ):
        response = api_client.create_order(DataTest.data_order_500, token=valid_token)
        assert response.status_code == 500


class TestReceivingOrdersFromSpecificUser:
    @allure.title("GET запрос - Получение заказов авторизованного пользователя")
    def test_get_orders_authorized(self, api_client, valid_token):
        response = api_client.get_orders(token=valid_token)
        assert response.status_code == 200
        assert "success" in response.json()

    @allure.title("GET запрос - Получение заказов не авторизованного пользователя")
    def test_get_orders_not_auth(self, api_client):
        response = api_client.get_orders()
        assert response.status_code == 401
        assert response.json() == ResponseBody.respons_body_not_auth
