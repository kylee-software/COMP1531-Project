import pytest
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.dm import dm_create_v1, dm_remove_v1
from src.error import InputError, AccessError

@pytest.fixture
def user0():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user1():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_dm_id(clear, user0):
    with pytest.raises(InputError):
        dm_remove_v1(user0['token'], 1) 
    clear_v1()

def test_invalid_token(clear, user0):
    owner_token = auth_register_v2("dmcreator@gmail.com", "TestTest1", "first", "last")['token']
    dm = dm_create_v1(owner_token, [user0['auth_user_id']])
    
    with pytest.raises(AccessError):
        dm_remove_v1("invalid.token.input", dm['dm_id'])
    clear_v1()

def test_not_creator(clear, user0):
    owner_token = auth_register_v2("dmcreator@gmail.com", "TestTest1", "first", "last")['token']
    dm = dm_create_v1(owner_token, [user0['auth_user_id']])
    
    with pytest.raises(AccessError):
        dm_remove_v1(user0['token'],dm['dm_id'])
    clear_v1()

def test_successful_remove(clear, user0):
    owner_token = auth_register_v2("dmcreator@gmail.com", "TestTest1", "first", "last")['token']
    dm = dm_create_v1(owner_token, [user0['auth_user_id']])
    
    assert dm_remove_v1(owner_token, dm['dm_id']) == {}
    clear_v1()