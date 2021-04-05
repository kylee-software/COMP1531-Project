import pytest


import pytest
import requests
from src import config

@pytest.fixture
def user():
    email = "test@unsw.au"
    password = "testPassword"
    firstname = "firstName"
    lastname = "lastName"
    response = requests.post(config.url + '/auth/register/v2', json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return response.json()

@pytest.fixture
def channel_id(user):
    response = requests.post(config.url + '/channels/create/v2', json={'token': user['token'], 'name': 'testChannel01', 'is_public': False})
    return response.json()['channel_id']

def test_one_user(user):
    requests.delete(config.url + '/clear/v1')
    response = requests.post(config.url + '/auth/logout/v1', json={'token': user['token']})
    assert response.status_code == 403

def test_one_channel(user, channel_id):
    requests.delete(config.url + '/clear/v1')
    response = requests.get(config.url + '/channels/listall/v2', params={'token': user['token']})    
    assert response.status_code == 403