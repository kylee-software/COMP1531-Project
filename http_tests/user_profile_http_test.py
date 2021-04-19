import pytest
import requests
from src.error import AccessError, InputError
from src import config
from src.auth import auth_register_v2
from src.other import clear_v1
import json

@pytest.fixture
def user():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)


@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

def test_invalid_token(clear, user):
    call = requests.get(config.url + 'user/profile/v2', params={'token' : 'testToken', 'u_id': user['auth_user_id']})
    assert call.status_code == 403

def test_invalid_user_id(clear, user):
    call = requests.get(config.url + 'user/profile/v2', params={'token' : user['token'], 'u_id': 5})
    assert call.status_code == 400 

def test_correct_output(clear, user):
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    user2 = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    user2 = json.loads(user2.text)
    p = {'token' : user['token'], 'u_id' : user2['auth_user_id']}
    call = requests.get(config.url + 'user/profile/v2', params=p)
    test_user = json.loads(call.text)['user']

    assert isinstance(test_user["u_id"], int)
    assert test_user["email"] == email
    assert test_user["name_first"] == firstname
    assert test_user["name_last"] == lastname
    assert test_user["handle_str"] == 'firstname2lastname2' 