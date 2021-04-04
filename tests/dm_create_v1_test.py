import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.dm import dm_create_v1
from src.error import InputError, AccessError

@pytest.fixture
def token():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstone"
    last_name = "lastone"
    token = auth_register_v2(email, password, first_name, last_name)['token']
    return token

@pytest.fixture
def user1():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firsttwo"
    last_name = "lasttwo"
    u_id = auth_register_v2(email, password, first_name, last_name)['auth_user_id']
    return u_id

@pytest.fixture
def user2():
    email = "testmail2@gamil.com"
    password = "Testpass1234567"
    first_name = "firstthree"
    last_name = "lastthree"
    u_id = auth_register_v2(email, password, first_name, last_name)['auth_user_id']
    return u_id

def test_invalid_token(user1):
    with pytest.raises(AccessError):
        dm_create_v1("Invalid token", [user1])
    clear_v1()

def test_invalid_u_ids(token, user1):
    with pytest.raises(InputError):
        dm_create_v1(token, [user1, 123])

    clear_v1()
    u_id = auth_register_v2("testemail@gmail.com", "testPassword1", "Removed", "user")['auth_user_id']
    with pytest.raises(InputError):
        dm_create_v1(token, [user1, u_id])
    clear_v1()

def test_valid_return(token, user1, user2):
    assert dm_create_v1(token, [user1])['dm_id'] == 1
    assert dm_create_v1(token, [user1, user2])['dm_id'] == 2
    clear_v1()

