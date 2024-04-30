from faker import Faker
import allure
import requests

#from data import DataTest
from constant import Constants


@allure.step("Получение json")
def json_user():
    fake = Faker()
    email = fake.email()
    password = fake.password()
    name = fake.name()
    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    return payload

@allure.step("Создание пользователя и получение его логина и пароля")
def log_user():
    fake = Faker()
    email = fake.email()
    password = fake.password()
    name = fake.name()
    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    json_log = {
        "email": email,
        "password": password
    }
    requests.post(Constants.url + Constants.creat_user, json = payload)
    return json_log

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

    request = requests.post(Constants.url + Constants.creat_user, json=payload)
    token_us = request.json()['accessToken']
    return token_us



