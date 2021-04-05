from src.error import AccessError
import jwt
from src.auth import auth_logout, auth_register_v2
from src.channels import channels_create_v2
from src.other import clear_v1
import pytest

def test_invalid_token():
    clear_v1()
    invalid_token = jwt.encode({'some' : 'value'}, "TestingSecret", algorithm='HS256')
    assert auth_logout(invalid_token) == False

def test_valid_token():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    token = auth_register_v2(email, password, firstname, lastname)['token']
    assert auth_logout(token) == True
    with pytest.raises(AccessError):
        channels_create_v2(token, 'testChannel', False)
