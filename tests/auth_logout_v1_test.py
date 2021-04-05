from src.error import AccessError
import jwt
from src.auth import auth_logout_v1, auth_register_v2
from src.channels import channels_create_v2
from src.other import clear_v1
import pytest

@pytest.fixture
def token():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email, password, firstname, lastname)['token']

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token():
    clear_v1()
    invalid_token = jwt.encode({'some' : 'value'}, "TestingSecret", algorithm='HS256')
    assert auth_logout_v1(invalid_token) == False

def test_correct_return(clear, token):    
    assert auth_logout_v1(token) == {'is_success': True}
    
def test_can_no_longer_access_other_functions(clear, token):
    auth_logout_v1(token)
    with pytest.raises(AccessError):
        channels_create_v2(token, 'testChannel', False)
