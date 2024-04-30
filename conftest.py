import pytest

from data import DataTest

@pytest.fixture()
def user_data():
    user_data = DataTest()
    return user_data