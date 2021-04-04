import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.auth import auth_register_v2

@pytest.fixture
def user1():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "first"
    lastname = "last"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def clear():
    clear_v1()

def test_user_profile_sethandle(clear, user1):
    '''
    A simple test to check user profile sethandle
    '''
    resp = requests.put(config.url + "user/profile/sethandle/v1", params={'token': user1['token'], 'handle_str':"newhandle"})
    assert resp.json() == {}

def test_user_sethandle_access_error(clear):
    resp = requests.put(config.url + "user/profile/sethandle/v1", params={'token': 'invalid.token.input', 'handle_str':"newhandle"})
    assert resp.status_code == 403

def test_user_sethandel_input_error(clear, user1):
    resp = requests.put(config.url + "user/profile/sethandle/v1", params={'token': user1['token'], 'handle_str':"newhandle"*1000})    
    assert resp.status_code == 400

