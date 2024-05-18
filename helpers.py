from faker import Faker
import allure
import requests

from urls import Urls


def generate_payloads():
    fake = Faker()
    email = fake.email()
    name = fake.name()
    password = fake.password()
    payload = {'email': email, 'password': password, 'name': name}
    login_payload = {'email': email, 'password': password}
    return payload, login_payload




@allure.step("Создание пользователя и получение его токена")
def token_user():
    fake = Faker()
    email = fake.email()
    password = fake.password()
    name = fake.name()
    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    request = requests.post(Urls.url + Urls.creat_user, json=payload)
    token_us = request.json()['accessToken']
    return token_us



