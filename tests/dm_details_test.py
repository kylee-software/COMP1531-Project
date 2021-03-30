import pytest
from src.auth import auth_register_v1
from src.error import AccessError, InputError
from src.dm import dm_details, dm_create
import jwt
from src.other import clear_v1

@pytest.fixture
def user_ids():
    u_ids = []
    for i in range(5):
        email = f"test{i}email@gmail.com"
        password = f"TestTest{i}"
        firstname = f"firstname{i}"
        lastname = f"lastname{i}"
        u_ids.append(auth_register_v1(email,password,firstname, lastname)['auth_user_id'])

@pytest.fixture
def tokens():
    tokens = []
    for i in range(5):
        email = f"test{i}email@gmail.com"
        password = f"TestTest{i}"
        firstname = f"firstname{i}"
        lastname = f"lastname{i}"
        tokens.append(auth_register_v1(email,password,firstname, lastname)['token'])
    
@pytest.fixture
def clear():
    clear_v1

def test_invalid_token(clear):
    with pytest.raises(AccessError):
        dm_details(jwt.encode({'test' : 'token'}, 'testSecret', algorithm='HS256'), 5)

def test_user_not_in_dm(clear, tokens, user_ids):
    dm = dm_create(tokens[1], user_ids[1:])
    with pytest.raises(AccessError):
        dm_details(tokens[0], dm['dm_id'])

def test_invalid_dm_id(clear, tokens):
    with pytest.raises(InputError):
        dm_details(tokens[0], 4)

def test_user_in_dm(clear, tokens, user_ids):
    dm = dm_create(tokens[1], user_ids[1:])
    assert len(dm_details(tokens[0], dm['dm_id'])) == 2
