from data import DataTest
import requests

from constant import Constants
data_log = DataTest.data_log_user
status_code = 200
def create_user(self, data_log, status_code):
    response = requests.post(Constants.url + Constants.login_user, json=data_log)
    expected_success = True
    actual_success = response.json()['success']
    assert response.status_code == status_code
    assert expected_success == actual_success