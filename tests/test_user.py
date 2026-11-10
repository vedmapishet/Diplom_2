import allure
import pytest

from data import DataTest, ResponseBody


class TestCreatingUser:
    @allure.title("POST запрос - Успешное создание пользователя")
    def test_create_user(self, user_data):
        response = user_data["response"]
        body = response.json()
        assert response.status_code == 200
        assert body["success"]
        assert "Bearer" in body["accessToken"]

    @allure.title(
        "POST запрос - Создание пользователя с неполными данными "
        "или уже зарегистрированным логином"
    )
    @pytest.mark.parametrize(
        ("data", "status_code", "expected_body"),
        [
            pytest.param(
                DataTest.data_403_not_name,
                403,
                ResponseBody.respons_body_403_not_all_fields,
                id="без имени",
            ),
            pytest.param(
                DataTest.data_403_not_password,
                403,
                ResponseBody.respons_body_403_not_all_fields,
                id="без пароля",
            ),
            pytest.param(
                DataTest.data_403_not_email,
                403,
                ResponseBody.respons_body_403_not_all_fields,
                id="без email",
            ),
            pytest.param(
                DataTest.data_403_replay,
                403,
                ResponseBody.respons_body_403_replay,
                id="повторная регистрация",
            ),
        ],
    )
    def test_create_user_fail(self, api_client, data, status_code, expected_body):
        response = api_client.register_user(data)
        assert response.status_code == status_code
        assert response.json() == expected_body


class TestLoginUser:
    @allure.title("POST запрос - Успешный логин пользователя")
    def test_user_login(self, api_client, user_data):
        response = api_client.login_user(user_data["login_payload"])
        body = response.json()
        assert response.status_code == 200
        assert body["success"]
        assert "Bearer" in body["accessToken"]

    @allure.title("POST запрос - НЕ успешный логин пользователя")
    @pytest.mark.parametrize(
        ("data", "status_code", "expected_body"),
        [
            pytest.param(
                DataTest.log_not_correct_user,
                401,
                ResponseBody.respons_body_not_login,
                id="несуществующий пользователь",
            ),
            pytest.param(
                DataTest.log_not_user,
                401,
                ResponseBody.respons_body_not_login,
                id="пустой email",
            ),
            pytest.param(
                DataTest.log_not_correct_password,
                401,
                ResponseBody.respons_body_not_login,
                id="неверный пароль",
            ),
            pytest.param(
                DataTest.log_not_password,
                401,
                ResponseBody.respons_body_not_login,
                id="пустой пароль",
            ),
        ],
    )
    def test_user_login_fail(self, api_client, data, status_code, expected_body):
        response = api_client.login_user(data)
        assert response.status_code == status_code
        assert response.json() == expected_body


class TestUpdateUser:
    @allure.title("PATCH запрос - Изменение НЕавторизованного пользователя")
    def test_update_user_not_authorized(self, api_client):
        response = api_client.update_user(
            DataTest.data_update, token=DataTest.headers_not_token["Authorization"]
        )
        assert response.status_code == 401
        assert response.json() == ResponseBody.respons_body_not_auth

    @allure.title("PATCH запрос - Успешное изменение авторизованного пользователя")
    def test_update_user(self, api_client, user_data):
        response = api_client.update_user(
            DataTest.data_update, token=user_data["token"]
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
