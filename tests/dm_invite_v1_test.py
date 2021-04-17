import pytest
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_invite_v1, dm_details_v1
from src.error import InputError, AccessError
from src.other import clear_v1, notifications_get_v1
import jwt
from src.helper import find_user, load_data

@pytest.fixture
def token():
    email = "test10email@gmail.com"
    password = "TestTest10"
    firstname = "firstname10"
    lastname = "lastname10"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user_id_list():
    u_ids = []
    for i in range(5):
        email = f"test{i}email@gmail.com"
        password = f"TestTest{i}"
        firstname = f"firstname{i}"
        lastname = f"lastname{i}"
        u_ids.append(auth_register_v2(email,password,firstname, lastname)['auth_user_id'])
    return u_ids

@pytest.fixture
def user2():
    email = "user2email@gmail.com"
    password = "Testuser2"
    firstname = "firstuser2"
    lastname = "lastuser2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def dm(token, user_id_list):
    return dm_create_v1(token['token'], user_id_list + [token['auth_user_id']])

def test_invalid_dm_id(clear, dm, token, user_id_list):
    with pytest.raises(InputError):
        dm_invite_v1(token['token'], 'invalid_dm_id', user_id_list[0])

def test_invalid_user_id(clear, dm, token, user_id_list):
    with pytest.raises(InputError):
        dm_invite_v1(token['token'], dm['dm_id'], 'invalid_user_id')

def test_invalid_token(clear, token, user_id_list):
    dm = dm_create_v1(token['token'], user_id_list[1:])
    with pytest.raises(AccessError):
        dm_invite_v1(jwt.encode({'Test': 'Token'}, 'TestSecret', algorithm='HS256'), dm['dm_id'], user_id_list[0])

def test_invited_user_is_already_in_dm(clear, dm, token, user_id_list):
    with pytest.raises(InputError):
        dm_invite_v1(token['token'], dm['dm_id'], user_id_list[0])

def test_auth_user_not_in_dm(clear, dm, token, user_id_list):
    email = "test91gmail@gmail.com"
    password = "TestTest91"
    firstname = "firstname91"
    lastname = "lastname91"
    token2 = auth_register_v2(email,password,firstname, lastname)['token']
    dm = dm_create_v1(token['token'], user_id_list[1:])
    with pytest.raises(AccessError):
        dm_invite_v1(token2, dm['dm_id'], user_id_list[0])

def test_everything_valid(clear, dm, token, user_id_list):
    dm = dm_create_v1(token['token'], user_id_list[1:])
    dm_invite_v1(token['token'], dm['dm_id'], user_id_list[0])
    assert len(dm_details_v1(token['token'], dm['dm_id'])['members']) == 6

def test_user_gets_notifications_when_invited(clear, dm, token, user2):
    dm_invite_v1(token['token'], dm['dm_id'], user2['auth_user_id'])
    notifications = notifications_get_v1(user2['token'])
    
    data = load_data()
    token_user = find_user(token['auth_user_id'], data)['account_handle']
    assert len(notifications['notifications']) == 1
    assert notifications['notifications'][0]['notification_message'] == f"{token_user} added you to {dm['dm_name']}"
    assert notifications['notifications'][0]['channel_id'] == -1
    assert notifications['notifications'][0]['dm_id'] == dm['dm_id']

