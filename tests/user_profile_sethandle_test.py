import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.user import user_profile_sethandle_v1, user_profile_v1

@pytest.fixture
def user1():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "first"
    lastname = "last"
    return auth_register_v1(email,password,firstname, lastname)


@pytest.fixture
def user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "first2"
    lastname = "last2"
    return auth_register_v1(email,password,firstname, lastname)

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear, user1):
    with pytest.raises(AccessError):
        user_profile_sethandle_v1('bad.token.input', 'newhandle')
    clear_v1()

def test_short_handle(clear, user1):
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], 'no')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], 'bad')
    clear_v1()

def test_long_handle(clear, user1):
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], 'handleiswaytoolongneedstobeshorter')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], 'handleisexactly20num')
    clear_v1()

def test_already_taken(clear, user1, user2):
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], "first2last2")
    clear_v1()

def test_valid_handle(clear, user1):
    # first check existing handle
    assert user_profile_v1(user1['token'], user1['auth_user_id'])['handle_str'] == 'firstlast'
    # change handle
    assert user_profile_sethandle_v1(user1['token'], "validhandle") == {}
    # check new handle has been saved
    assert user_profile_v1(user1['token'], user1['auth_user_id'])['handle_str'] == 'validhandle'

#assuming if they are trying to change to the same handle they already have nothing happens but it returns successful
def test_same_handle(clear, user1):
    assert user_profile_v1(user1['token'], user1['auth_user_id'])['handle_str'] == 'firstlast'
    assert user_profile_sethandle_v1(user1['token'], "firstlast") == {}
    assert user_profile_v1(user1['token'], user1['auth_user_id'])['handle_str'] == 'firstlast'