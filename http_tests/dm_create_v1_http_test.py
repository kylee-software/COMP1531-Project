import pytest
import requests
from src import config

@pytest.fixture
def token():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstone"
    last_name = "lastone"
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()

    token = resp['token']
    return token

@pytest.fixture
def user1():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firsttwo"
    last_name = "lasttwo"
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()

    u_id = resp['auth_user_id']
    return u_id

@pytest.fixture
def user2():
    email = "testmail2@gamil.com"
    password = "Testpass1234567"
    first_name = "firstthree"
    last_name = "lastthree"
    resp = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()

    u_id = resp['auth_user_id']
    return u_id

def test_invalid_token(user1):
    status_code = requests.post(config.url + 'dm/create/v1', json={
        'token': "invalid_token",
        'u_ids': [user1]
    }).status_code

    assert status_code == 403  # Status code for AccessError
    requests.delete(config.url + 'clear/v1')

def test_invalid_u_ids(token, user1):
    status_code1 = requests.post(config.url + 'dm/create/v1', json={
        'token': token,
        'u_ids': [user1, 123]
    }).status_code

    u_id = requests.post(config.url + 'auth/register/v2', json={
        'email': "testemail@gmail.com",
        'password': "testPassword1",
        'name_first': "Removed",
        'name_last': "user"
    }).json()['auth_user_id']

    requests.delete(config.url + 'clear/v1')

    status_code2 = requests.post(config.url + 'dm/create/v1', json={
        'token': token,
        'u_ids': [user1, u_id]
    }).status_code

    assert status_code1 == 400  # Status code for InputError
    assert status_code2 == 400
    requests.delete(config.url + 'clear/v1')

def test_valid_return(token, user1, user2):
    dm_id1 = requests.post(config.url + 'dm/create/v1', json={
        'token': token,
        'u_ids': [user1]
    }).json()['dm_id']

    dm_id2 = requests.post(config.url + 'dm/create/v1', json={
        'token': token,
        'u_ids': [user1, user2]
    }).json()['dm_id']

    assert dm_id1 == 1
    assert dm_id2 == 2

    requests.delete(config.url + 'clear/v1')