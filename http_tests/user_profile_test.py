import pytest
import requests
from src import auth
from src.error import AccessError
from src import config
from src.auth import auth_register_v1

def test_invalid_token():
    with pytest.raises(AccessError):
        requests.get(config.url + '/user/profile/v2', params={'token' : {'test' : 'token'}})

def test_correct_output():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    token = auth_register_v1(email,password,firstname, lastname)['auth_user_id']
    user = requests.get(config.url + '/user/profile/v2', params={'token' : token})['user']
    assert user['u_id'].is_integer()
    assert user['email'] == email
    assert user['name_first'] == firstname
    assert user['name_last'] == lastname
    assert user['handle_str'] == 'firstname1lastname1'