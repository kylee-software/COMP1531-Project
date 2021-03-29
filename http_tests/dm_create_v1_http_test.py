import pytest
import requests
from src import config

@pytest.fixture
def token():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstone"
    last_name = "lastone"
    token = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['token']

    return token

@pytest.fixture
def user1():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firsttwo"
    last_name = "lasttwo"
    u_id = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['auth_user_id']

    return u_id

@pytest.fixture
def user2():
    email = "testmail2@gamil.com"
    password = "Testpass1234567"
    first_name = "firstthree"
    last_name = "lastthree"
    u_id = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['auth_user_id']
    return u_id

def test_invalid_token(user1):
    status_code = requests.post(config.url + 'dm/create/v1', json={
        'token': "Invalid token",
        'u_ids': [user1]
    }).status_code

    assert status_code == 403  # Status code for AccessError

def test_invalid_u_id(token, user1):
    status_code = requests.post(config.url + 'dm/create/v1', json={
        'token': token,
        'u_ids': [user1, 123]
    }).status_code

    assert status_code == 400  # Status code for InputError

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

    # Reset data
    requests.delete(config.url + 'clear/v1').json()