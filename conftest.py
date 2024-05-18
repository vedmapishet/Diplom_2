import requests
import pytest
from faker import Faker
from urls import *
from helpers import generate_payloads


@pytest.fixture(scope='function')
def user_data():
    payload, login_payload = generate_payloads()
    response = requests.post(Urls.url + Urls.creat_user, data=payload)
    token = response.json()['accessToken']
    yield {'login_payload': login_payload, 'token': token, 'response': response}
    headers = {'Authorization': token}
    requests.delete(Urls.url + Urls.auth_user, headers=headers)