import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.auth import auth_register_v2

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
    resp = requests.post(config.url + "admin/userpermission/change/v1", json={'token': user1['token'], 'u_id':user2['auth_user_id'], 'permission_id':1})
    assert resp.json() == {}
    
def test_admin_permissions_access_error(clear, user2):
    resp = requests.post(config.url + "admin/userpermission/change/v1", json={'token': 'invalid.token.input', 'u_id':user2['auth_user_id'], 'permission_id':OWNER_PERMISSION})
    assert resp.status_code == 403

def test_admin_permissions_input_error(clear, user1):
    invalid_id = user1['auth_user_id'] + 1
    resp = requests.post(config.url + "admin/userpermission/change/v1", json={'token': user1['token'], 'u_id': invalid_id, 'permission_id':OWNER_PERMISSION})
    assert resp.status_code == 400



