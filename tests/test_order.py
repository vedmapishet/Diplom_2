import allure
import pytest
import requests

from data import DataTest
from urls import Urls
from data import ResponsBody

class TestCreatingOrder:
    @allure.title('POST запрос - Успешное создание заказа с авторизацией')
    def test_create_order(self, user_data):
        user = user_data['response']
        headers = {'Authorization': user.json()['accessToken']}
        response = requests.post(Urls.url + Urls.orders, data=DataTest.data_order, headers=headers)
        r = response.json()
        assert r['success'] and response.status_code == 200




    @allure.title('POST запрос - НЕуспешное создание заказа')
    @pytest.mark.parametrize(("data", "status_code", "headers", "json"), [
        (
                pytest.param(DataTest.data_order_not_ingredients, 400, DataTest.headers, ResponsBody.respons_body_not_ingredients)
        ),
        (
                pytest.param(DataTest.data_order_not_ingredients, 400, DataTest.not_headers, ResponsBody.respons_body_not_ingredients)
        )
    ])
    def test_create_order_not_ingredients(self, data, status_code, headers, json):
        response = requests.post(Urls.url + Urls.orders, json=data, headers=headers)
        assert response.status_code == status_code and json == response.json()



    @allure.title('POST запрос - НЕуспешное создание заказа с неверным хешем ингредиентов')
    @pytest.mark.parametrize(("data", "status_code", "headers"), [
        (
                pytest.param(DataTest.data_order_500, 500, DataTest.headers)
        )
    ])
    def test_create_order_with_an_incorrect_hash_of_ingredients(self, data, status_code, headers):
        response = requests.post(Urls.url + Urls.orders, json=data, headers=headers)
        assert response.status_code == status_code

class TestReceivingOrdersFromSpecificUser:
    @allure.title('POST запрос - Получение заказов авторизованного пользователя')
    @pytest.mark.parametrize(("status_code", "headers"), [
        (
                pytest.param(200, DataTest.headers)
        )
    ])
    def test_create_order_with_an_incorrect_hash_of_ingredients(self, status_code, headers):
        response = requests.get(Urls.url + Urls.orders, headers=headers)
        assert response.status_code == status_code and 'success' in response.json()

    @allure.title('POST запрос - Получение заказов не авторизованного пользователя')
    @pytest.mark.parametrize(("status_code", "json"), [
        (
                pytest.param(401, ResponsBody.respons_body_not_auth)
        )
    ])
    def test_create_order_with_an_incorrect_hash_of_ingredients_not_auth(self, status_code, json):
        response = requests.get(Urls.url + Urls.orders)
        assert response.status_code == status_code and json == response.json()

