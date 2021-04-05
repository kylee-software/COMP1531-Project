import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.admin import admin_changepermission_v1

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

@pytest.fixture
def user3():
    email = "test3email@gmail.com"
    password = "TestTest3"
    firstname = "firstname3"
    lastname = "lastname3"
    return auth_register_v2(email,password,firstname, lastname)

def test_invalid_u_id(clear, user1):
    with pytest.raises(InputError):
        invalid_id = user1['auth_user_id'] + 1
        admin_changepermission_v1(user1['token'], invalid_id, OWNER_PERMISSION)

def test_invalid_token(clear, user1):
    with pytest.raises(AccessError):
        admin_changepermission_v1('invalid.token.input', user1['auth_user_id'], OWNER_PERMISSION)

def test_not_global_owner(clear, user1, user2):
    with pytest.raises(AccessError):
        admin_changepermission_v1(user2['token'], user1['auth_user_id'], OWNER_PERMISSION)

def test_invalid_permission_id(clear, user1, user2):
    with pytest.raises(InputError):
        admin_changepermission_v1(user1['token'], user2['auth_user_id'], INVALID_PERMISSION)

def test_change_to_owner(clear, user1, user2, user3):
    with pytest.raises(AccessError):
        admin_changepermission_v1(user2['token'], user3['auth_user_id'], OWNER_PERMISSION)  

    assert admin_changepermission_v1(user1['token'], user2['auth_user_id'], OWNER_PERMISSION) == {}
    assert admin_changepermission_v1(user2['token'], user3['auth_user_id'], OWNER_PERMISSION) == {}
    clear_v1()

def test_change_to_not_owner(clear, user1, user2, user3):
    #first assert ensures user1 is an owner (they can change user2's permission)
    assert admin_changepermission_v1(user1['token'], user2['auth_user_id'], OWNER_PERMISSION) == {}
    #now we reset user1's permission to member
    assert admin_changepermission_v1(user2['token'], user1['auth_user_id'], MEMBER_PERMISSION) == {}
    
    #if the permission successfully reset they can't change permissions anymore
    with pytest.raises(AccessError):
        admin_changepermission_v1(user1['token'], user3['auth_user_id'], OWNER_PERMISSION)  


