import requests
import pytest
from requests.api import delete
from src import config

@pytest.fixture
def user():
    email = "tesmail@gmail.com"
    firstname = "testName"
    lastname = "lastName"
    password = "testPass4"
    user = requests.post(config.url + '/auth/register/v2', json={'email': email, 'name_first': firstname,
                                                        'name_last': lastname, 'password': password})
    return user.json()

@pytest.fixture
def user2():
    email = "tesmail2@gmail.com"
    firstname = "testName2"
    lastname = "lastName2"
    password = "testPass4"
    user = requests.post(config.url + '/auth/register/v2', json={'email': email, 'name_first': firstname,
                                                        'name_last': lastname, 'password': password})
    return user.json()

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

@pytest.fixture
def dm_id(user):
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user['token'],
        'u_ids': [user['auth_user_id']]})
    return dm.json()['dm_id']

def test_invalid_token(clear, user, user2, dm_id):
    response = requests.post(config.url + '/dm/invite/v1', json={'token': 'test_token', 'dm_id': dm_id, 'u_id': user2['auth_user_id']})
    assert response.status_code == 403

def test_invalid_dm_id(clear, user, user2):
    response = requests.post(config.url + '/dm/invite/v1', json={'token': user['token'], 'dm_id': 'test_id', 'u_id': user2['auth_user_id']})
    assert response.status_code == 400

def test_invalid_user_id(clear, user, dm_id):
    response = requests.post(config.url + '/dm/invite/v1', json={'token': user['token'], 'dm_id': dm_id, 'u_id': 'test_id'})
    assert response.status_code == 400

def test_invalid_auth_user_not_in_dm(clear, user, user2, dm_id):
    response = requests.post(config.url + '/dm/invite/v1', json={'token': user2['token'], 'dm_id': dm_id, 'u_id': user2['auth_user_id']})
    assert response.status_code == 403

def test_everything_valid(clear, user, user2, dm_id):
    requests.post(config.url + '/dm/invite/v1', json={'token': user['token'], 'dm_id': dm_id, 'u_id': user2['auth_user_id']})
    details = requests.get(config.url + '/dm/details/v1', params={'token': user['token'], 'dm_id': dm_id})
    assert len(details.json()['members']) == 2