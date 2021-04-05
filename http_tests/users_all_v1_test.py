import pytest
from src.other import clear_v1
import requests
from src import config
from src.error import AccessError

@pytest.fixture
def create_users():
    for i in range(5):
        email = f"test{i}email@gmail.com"
        password = f"TestTest{i}"
        firstname = f"firstname{i}"
        lastname = f"lastname{i}"
        token = requests.post(config.url + '/auth/register/v2', json={'email': email,
                                                            'password': password,
                                                            'name_first': firstname,
                                                            'name_last': lastname,
                                                            })
    return token.json()['token']

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

def returns_4_users(clear, create_users):
    list = requests.get(config.url +'/users/all/v1', params={'token' : create_users})
    assert len(list.json()['users']) == 4

def invalid_token(clear, create_users):
    response = requests.get(config.url + '/users/all/v1', params={'token' : {'test' : 'token'}})
    assert response.status_code == 403
