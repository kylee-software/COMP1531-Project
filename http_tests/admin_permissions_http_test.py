import pytest
import requests
import json
from src import config

OWNER_PERMISSION = 1
MEMBER_PERMISSION = 2
INVALID_PERMISSION = 3

@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def user1():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

def test_admin_permissions_change(clear, user1, user2):
    '''
    A simple test to check admin permissions
    '''
    resp = requests.post(config.url + 'echo', params={'token': user1['token'], 'u_id':user2['auth_user_id'], 'permission_id':OWNER_PERMISSION})
    assert json.loads(resp.text) == {}
    resp = requests.post(config.url + 'echo', params={'token': 'invalid.token.input', 'u_id':user2['auth_user_id'], 'permission_id':OWNER_PERMISSION})
    assert resp.status_code == 400



