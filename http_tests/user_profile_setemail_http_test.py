import pytest
import requests
import json
from src import config

@pytest.fixture
def user():
    email = "testmail@gmail.com"
    password = "Testpass1"
    first_name = "firstone"
    last_name = "lastone"
    token = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['token']
    return token

def test_invalid_token():
    status_code = requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': "invalid_token",
        'email': "testemail@gmail.com",
    }).status_code
    assert status_code == 403

def test_invalid_email(user):
    status_code = requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': user,
        'email': "testemail.com",
    }).status_code

    assert status_code == 400
    requests.delete(config.url + '/clear/v1')

def test_email_existed(user):
    status_code = requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': user,
        'email': "testmail@gmail.com",
    }).status_code

    assert status_code == 400
    requests.delete(config.url + '/clear/v1')

def test_correct_setup(user):
    requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': user,
        'email': "newemail@gmail.com",
    })

    status_code = requests.put(config.url + 'user/profile/setemail/v2', json={
        'token': user,
        'email': "newemail@gmail.com",
    }).status_code

    assert status_code == 400
    requests.delete(config.url + '/clear/v1')