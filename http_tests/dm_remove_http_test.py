import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.dm import dm_create_v1

@pytest.fixture
def user0():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def clear():
    clear_v1()

def test_dm_remove(clear, user0):
    owner_token = auth_register_v2("dmcreator@gmail.com", "TestTest1", "first", "last")['token']
    dm = dm_create_v1(owner_token, [user0['auth_user_id']])
    resp = requests.delete(config.url + 'dm/remove/v1', json={'token': owner_token, 'dm_id':dm['dm_id']})
    assert resp.json() == {}

def test_dm_remove_access_error(clear, user0):
    owner_token = auth_register_v2("dmcreator@gmail.com", "TestTest1", "first", "last")['token']
    dm = dm_create_v1(owner_token, [user0['auth_user_id']])
    resp = requests.delete(config.url + 'dm/remove/v1', json={'token': 'bad.token.input', 'dm_id':dm['dm_id']})
    assert resp.status_code == 403

def test_dm_remove_input_error(clear, user0):
    owner_token = auth_register_v2("dmcreator@gmail.com", "TestTest1", "first", "last")['token']
    dm = dm_create_v1(owner_token, [user0['auth_user_id']])
    resp = requests.delete(config.url + 'dm/remove/v1', json={'token': owner_token, 'dm_id':dm['dm_id'] + 1})
    assert resp.status_code == 400