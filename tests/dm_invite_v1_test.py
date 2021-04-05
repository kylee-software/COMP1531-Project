import pytest
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_invite, dm_details_v1
from src.error import InputError, AccessError
from src.other import clear_v1
import jwt

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
def clear():
    clear_v1()


def test_invalid_dm_id(clear, token, user_id_list):
    with pytest.raises(InputError):
        dm_invite(token['token'], 'invalid_dm_id', user_id_list[0])

def test_invalid_user_id(clear, token, user_id_list):
    dm = dm_create_v1(token['token'], user_id_list)
    with pytest.raises(InputError):
        dm_invite(token['token'], dm['dm_id'], 'invalid_user_id')

def test_invalid_token(clear, token, user_id_list):
    dm = dm_create_v1(token['token'], user_id_list[1:])
    with pytest.raises(AccessError):
        dm_invite(jwt.encode({'Test': 'Token'}, 'TestSecret', algorithm='HS256'), dm['dm_id'], user_id_list[0])

def test_invited_user_is_already_in_dm(clear, token, user_id_list):
    dm = dm_create_v1(token['token'], user_id_list)
    with pytest.raises(InputError):
        dm_invite(token['token'], dm['dm_id'], user_id_list[0])

def test_user_not_in_dm(clear, token, user_id_list):
    email = "test91gmail@gmail.com"
    password = "TestTest91"
    firstname = "firstname91"
    lastname = "lastname91"
    token2 = auth_register_v2(email,password,firstname, lastname)['token']
    dm = dm_create_v1(token['token'], user_id_list[1:])
    with pytest.raises(AccessError):
        dm_invite(token2, dm['dm_id'], user_id_list[0])

def test_everything_valid(clear, token, user_id_list):
    dm = dm_create_v1(token['token'], user_id_list[1:] + [token['auth_user_id']])
    dm_invite(token['token'], dm['dm_id'], user_id_list[0])
    assert len(dm_details_v1(token['token'], dm['dm_id'])['members']) == 6
