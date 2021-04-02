import pytest
import requests
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.other import clear_v1
from src.user import user_profile_v2

@pytest.fixture
def user():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v2(email, password, firstname, lastname)

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear, user):
    with pytest.raises(AccessError):
        user_profile_v2({'test':'token'}, user['auth_user_id'])

def test_invalid_user_id(clear, user):
    with pytest.raises(InputError):
        user_profile_v2(user['token'],  4)

def test_correct_output(clear, user):
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    user_details = auth_register_v2(email,password, firstname, lastname)

    test_user = user_profile_v2(user['token'], user_details['auth_user_id'])['user']
    
    assert isinstance(test_user['u_id'], int)
    assert test_user['email'] == email
    assert test_user['name_first'] == firstname
    assert test_user['name_last'] == lastname
    assert test_user['handle_str'] == 'firstname2lastname2'