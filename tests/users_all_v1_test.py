from os import access
import pytest
from src.error import AccessError
from src.auth import auth_register_v2
from src.other import clear_v1
from src.user import users_all_v1
from src.admin import admin_user_remove_v1

@pytest.fixture
def token():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)['token']

@pytest.fixture
def token1():
    email = "testemai333l@gmail.com"
    password = "TestTest3333"
    firstname = "firstname333"
    lastname = "lastname33"
    return auth_register_v2(email,password,firstname, lastname)['auth_user_id']

@pytest.fixture
def users():
    for i in range(5):
        email = f"test{i}email@gmail.com"
        password = f"TestTest{i}"
        firstname = f"firstname{i}"
        lastname = f"lastname{i}"
        id = auth_register_v2(email,password,firstname, lastname)
    return id['auth_user_id']


@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear):
    with pytest.raises(AccessError):
        users_all_v1('token')

def test_return_6_users(clear, token, users):
    u_list = users_all_v1(token)
    assert len(u_list['users']) == 6

def test_5_users_1_removed(clear, token, users):
    admin_user_remove_v1(token, users)
    assert len(users_all_v1(token)['users']) == 5

def test_proper_dict_values(clear, token, users):
    u_list = users_all_v1(token)
    assert len(u_list) == 1
    assert 'users' in u_list
    assert 'u_id' in u_list['users'][0]
    assert 'email' in u_list['users'][0]
    assert 'name_first' in u_list['users'][0]
    assert 'name_last' in u_list['users'][0]
    assert 'handle_str' in u_list['users'][0]