import pytest
from src.auth import auth_register_v2
from src.error import AccessError, InputError
from src.dm import dm_details_v1, dm_create_v1
import jwt
from src.other import clear_v1

@pytest.fixture
def num_members():
    return 5

@pytest.fixture
def users(num_members):

    u_ids = []
    tokens = []
    for i in range(num_members):
        email = f"test{i}email@gmail.com"
        password = f"TestTest{i}"
        firstname = f"firstname{i}"
        lastname = f"lastname{i}"
        user = auth_register_v2(email,password,firstname, lastname)
        u_ids.append(user['auth_user_id'])
        tokens.append(user['token'])
    return {'tokens' : tokens, 'u_ids': u_ids}

    
@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear):
    with pytest.raises(AccessError):
        dm_details_v1(jwt.encode({'test' : 'token'}, 'testSecret', algorithm='HS256'), 5)

def test_user_not_in_dm(clear, users):
    dm = dm_create_v1(users['tokens'][1], users['u_ids'][1:])
    with pytest.raises(AccessError):
        dm_details_v1(users['tokens'][0], dm['dm_id'])

def test_invalid_dm_id(clear, users):
    with pytest.raises(InputError):
        dm_details_v1(users['tokens'][0], 'test_dm_id')

def test_user_in_dm(clear, users, num_members):
    dm = dm_create_v1(users['tokens'][0], users['u_ids'])
    details = dm_details_v1(users['tokens'][1], dm['dm_id'])
    assert len(details) == 2
    assert len(details['members']) == num_members

def test_valid_dict_keys(clear, users):
    dm = dm_create_v1(users['tokens'][0], users['u_ids'])
    details = dm_details_v1(users['tokens'][1], dm['dm_id'])
    assert 'names' and 'members' in details 
    assert 'user_id' in details['members'][0] 
    assert 'email' in details['members'][0] 
    assert 'name_first' in details['members'][0] 
    assert 'name_last' in details['members'][0]
    assert 'handle_str' in details['members'][0] 

