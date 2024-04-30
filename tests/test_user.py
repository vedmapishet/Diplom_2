import allure
import pytest
import requests

from data import DataTest
from constant import Constants
from data import ResponsBody

class TestCreatingUser:
    @allure.title('POST запрос - Успешное создание пользователя')
    @pytest.mark.parametrize(("data", "status_code"), [
        (
                pytest.param(DataTest.data_us, 200)
        )
    ])
    def test_create_user(self, data, status_code):
        response = requests.post(Constants.url + Constants.creat_user, json=data)
        assert response.status_code == status_code
        assert 'accessToken' in response.text

    @allure.title(
        'POST запрос - Тестирование заполнения всех полей и создание пользователя с логином, который уже зарегистрирован')
    @pytest.mark.parametrize(("data", "status_code", "json"), [
        (
                pytest.param(DataTest.data_403_not_name, 403,
                             ResponsBody.respons_body_403_not_all_fields)
        ),
        (
                pytest.param(DataTest.data_403_not_password, 403,
                             ResponsBody.respons_body_403_not_all_fields)
        ),
        (
                pytest.param(DataTest.data_403_not_email, 403,
                             ResponsBody.respons_body_403_not_all_fields)
        ),
        (
                pytest.param(DataTest.data_403_replay, 403,
                             ResponsBody.respons_body_403_replay)
        )
    ])
    def test_create_user_fail(self, data, status_code, json):
        response = requests.post(Constants.url + Constants.creat_user, json=data)
        assert response.status_code == status_code and response.text == json

class TestLoginUser:
    @allure.title('POST запрос - Успешный логин пользователя')
    @pytest.mark.parametrize(("data", "status_code"), [
        (
                pytest.param(DataTest.data_log_user, 200)
        )
    ])
    def test_user_login(self, data, status_code):
        response = requests.post(Constants.url + Constants.login_user, json=data)
        expected_success = True
        actual_success = response.json()['success']
        assert response.status_code == status_code
        assert expected_success == actual_success

    @allure.title('POST запрос - НЕ успешный логин пользователя')
    @pytest.mark.parametrize(("data", "status_code", "json"), [
        (
                pytest.param(DataTest.log_not_correct_user, 401, ResponsBody.respons_body_not_login)
        ),
        (
                pytest.param(DataTest.log_not_user, 401, ResponsBody.respons_body_not_login)
        ),
        (
                pytest.param(DataTest.log_not_correct_password, 401, ResponsBody.respons_body_not_login)
        ),
        (
                pytest.param(DataTest.log_not_password, 401, ResponsBody.respons_body_not_login)
        )
    ])
    def test_user_login_fail(self, data, status_code, json):
        response = requests.post(Constants.url + Constants.login_user, json=data)
        assert response.status_code == status_code and json == response.json()

class TestUpdateUser:
    @allure.title('PATCH запрос - Изменение НЕавторизованного пользователя')
    @pytest.mark.parametrize(("data", "status_code", "json", "token"), [
        (
                pytest.param(DataTest.data_update, 401, ResponsBody.respons_body_not_auth, DataTest.headers_not_token)
        )
    ])
    def test_create_user(self, data, status_code, json, token):
        response = requests.patch(Constants.url + Constants.auth_user, json=data, headers=token)
        assert response.status_code == status_code
        assert json == response.json()

    @allure.title('PATCH запрос - Успешное изменение авторизованного пользователя')
    @pytest.mark.parametrize(("data", "status_code", "headers"), [
        (
                pytest.param(DataTest.data_update, 200, DataTest.headers)
        )
    ])
    def test_create_user(self, data, status_code, headers):
        response = requests.patch(Constants.url + Constants.auth_user, headers = headers, json=data)
        assert response.status_code == status_code and response.json()['success'] is True