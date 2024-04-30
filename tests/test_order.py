import allure
import pytest
import requests

from data import DataTest
from constant import Constants
from data import ResponsBody

class TestCreatingOrder:
    @allure.title('POST запрос - Успешное создание заказа с авторизацией')
    @pytest.mark.parametrize(("data", "status_code", "headers", "json"), [
        (
                pytest.param(DataTest.data_order, 200, DataTest.headers, ResponsBody.respons_body_not_ingredients)
        )
    ])
    def test_create_order(self, data, status_code, headers, json):
        response = requests.post(Constants.url + Constants.orders, json=data, headers=headers)
        status = response.json()['success']
        assert response.status_code == status_code and status == True

    @allure.title('POST запрос - Успешное создание заказа БЕЗ авторизации')
    @pytest.mark.parametrize(("data", "status_code", "json"), [
        (
                pytest.param(DataTest.data_order, 200, ResponsBody.respons_body_403_replay)
        )
    ])
    def test_create_order_not_auth(self, data, status_code, json):
        response = requests.post(Constants.url + Constants.orders, json=data)
        assert response.status_code == status_code


    @allure.title('POST запрос - НЕуспешное создание заказа (без ингридиентов)')
    @pytest.mark.parametrize(("data", "status_code", "headers", "json"), [
        (
                pytest.param(DataTest.data_order_not_ingredients, 400, DataTest.headers, ResponsBody.respons_body_not_ingredients)
        )
    ])
    def test_create_order_not_ingredients(self, data, status_code, headers, json):
        response = requests.post(Constants.url + Constants.orders, json=data, headers=headers)
        assert response.status_code == status_code and json == response.json()

    @allure.title('POST запрос - НЕуспешное создание заказа (без ингридиентов)')
    @pytest.mark.parametrize(("data", "status_code", "json"), [
        (
                pytest.param(DataTest.data_order_not_ingredients, 400, ResponsBody.respons_body_not_ingredients)
        )
    ])
    def test_create_order_not_ingredients_not_auth(self, data, status_code, json):
        response = requests.post(Constants.url + Constants.orders, json=data)
        assert response.status_code == status_code and json == response.json()

    @allure.title('POST запрос - НЕуспешное создание заказа с неверным хешем ингредиентов')
    @pytest.mark.parametrize(("data", "status_code", "headers"), [
        (
                pytest.param(DataTest.data_order_500, 500, DataTest.headers)
        )
    ])
    def test_create_order_with_an_incorrect_hash_of_ingredients(self, data, status_code, headers):
        response = requests.post(Constants.url + Constants.orders, json=data, headers=headers)
        assert response.status_code == status_code

class TestReceivingOrdersFromSpecificUser:
    @allure.title('POST запрос - Получение заказов авторизованного пользователя')
    @pytest.mark.parametrize(("status_code", "headers"), [
        (
                pytest.param(200, DataTest.headers)
        )
    ])
    def test_create_order_with_an_incorrect_hash_of_ingredients(self, status_code, headers):
        response = requests.get(Constants.url + Constants.orders, headers=headers)
        assert response.status_code == status_code and 'success' in response.json()

    @allure.title('POST запрос - Получение заказов не авторизованного пользователя')
    @pytest.mark.parametrize(("status_code", "json"), [
        (
                pytest.param(401, ResponsBody.respons_body_not_auth)
        )
    ])
    def test_create_order_with_an_incorrect_hash_of_ingredients_not_auth(self, status_code, json):
        response = requests.get(Constants.url + Constants.orders)
        assert response.status_code == status_code and json == response.json()

