import jwt
from src.auth import auth_logout, auth_register_v1

def test_invalid_token():
    invalid_token = jwt.encode({'some' : 'value'}, "TestingSecret", algorithm='HS256')
    assert auth_logout(invalid_token) == False

def test_valid_token():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    token = auth_register_v1(email,password,firstname, lastname)
    assert auth_logout(token) == True