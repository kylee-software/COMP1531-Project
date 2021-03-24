import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
import requests
from src import config
from src.error import AccessError

@pytest.fixture
def create_users():
    clear_v1()
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    auth_register_v1(email, password, firstname, lastname)
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    auth_register_v1(email, password, firstname, lastname)
    email = "test3email@gmail.com"
    password = "TestTest3"
    firstname = "firstname3"
    lastname = "lastname3"
    auth_register_v1(email, password, firstname, lastname)
    email = "test4email@gmail.com"
    password = "TestTest4"
    firstname = "firstname4"
    lastname = "lastname4"
    return auth_register_v1(email, password, firstname, lastname)

def returns_4_users(create_user):
    assert len(requests.get(config.url +'/users/all/v1', params={'token' : create_user})) == 4

def invalid_token():
    clear_v1()
    with pytest.raises(AccessError):
        requests.get(config.url + '/users/all/v1', params={'token' : {'test' : 'token'}})

