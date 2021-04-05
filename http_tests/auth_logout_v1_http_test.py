import requests
import pytest
from src import config

@pytest.fixture
def token():
    email = "test@unsw.au"
    password = "testPassword"
    firstname = "firstName"
    lastname = "lastName"
    response = requests.post(config.url + '/auth/register/v2', json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return response.json()['token']

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

def test_invalid_token(clear):
    response = requests.post(config.url + '/auth/logout/v1', json={'token': 'token'})
    assert response.status_code == 403

def test_valid_response(clear, token):
    response = requests.post(config.url + '/auth/logout/v1', json={'token': token})
    assert response.json()['is_success'] == True
