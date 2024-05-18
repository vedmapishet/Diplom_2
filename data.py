from helpers import token_user

from urls import Urls




class DataTest:
    not_headers = {
        "Content-Type": "application/json"
    }

    headers_not_token = {
        "Content-Type": "application/json",
        "Authorization": Urls.token
    }

    header = token_user()
    headers = {
        "Content-Type": "application/json",
        "Authorization": header
    }

    data_not_fields_are_not_filled = {
        "email": "",
        "password": "",
        "name": ""
    }

    data_update = {
        "user": {
            "email": "test-data@yandex.ru",
            "name": "name"
        }
    }

    data_403_not_name = {
        "email": "test-data@yandex.ru",
        "password": "name",
    }

    data_403_not_password = {
        "email": "test-data@yandex.ru",
        "name": "name"
    }
    data_403_not_email = {
        "password": "password",
        "name": "name"
    }

    data_403_replay = {
        "email": "test-data@yandex.ru",
        "password": "password",
        "name": "Username"
    }

    log_not_correct_user = {
        "email": "data@ya222.ru",
        "password": "password"
    }

    log_not_user = {
        "email": "",
        "password": "password"
    }

    log_not_correct_password = {
        "email": "data@ya22.ru",
        "password": "pass"
    }
    log_not_password = {
        "email": "data@ya22.ru",
        "password": ""
    }

    data_order_not_ingredients = {}
    data_order_500 = {
        "ingredients": [11]
    }

    data_order = {"ingredients": ["61c0c5a71d1f82001bdaaa72", "61c0c5a71d1f82001bdaaa73", "61c0c5a71d1f82001bdaaa6d"]}




class ResponsBody:
    respons_body = {"ok": True}
    respons_body_403_replay = '{"success":false,"message":"User already exists"}'
    respons_body_403_not_all_fields = '{"success":false,"message":"Email, password and name are required fields"}'
    respons_body_404 = {"code": 404, "message": "Курьера с таким id нет."}
    respons_body_500 = {"code":500,"message":"invalid input syntax for type integer: \":id\""}
    respons_body_not_login = {'success': False, 'message': "email or password are incorrect"}
    respons_body_not_auth = {"success": False, "message": "You should be authorised"}
    respons_body_not_ingredients = {"success": False, "message": "Ingredient ids must be provided"}
