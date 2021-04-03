import pytest
import requests
from src import config
from src.error import AccessError, InputError
import jwt

@pytest.fixture
def users():

    u_ids = []
    tokens = []
    for i in range(5):
        email = f"test{i}email@gmail.com"
        password = f"TestTest{i}"
        firstname = f"firstname{i}"
        lastname = f"lastname{i}"
        user = requests.post(config.url + 'auth/register/v2', json={
                                                                    'email': email,
                                                                    'password': password,
                                                                    'name_first': firstname,
                                                                    'name_last': lastname,
                                                                    })
        user = user.json()
        u_ids.append(user['auth_user_id'])
        tokens.append(user['token'])

    return {'tokens' : tokens, 'u_ids': u_ids}
    
@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

def test_invalid_token(clear, users):
    dm = requests.post(config.url + 'dm/create/v1', json={'token': users['tokens'][0], 'u_ids': users['u_ids']})
    dm = dm.json()
    p = {'token' : jwt.encode({'test' : 'token'}, 'testSecret', algorithm='HS256'), 'dm_id' : dm['dm_id']}
    with pytest.raises(AccessError):
        requests.get(config.url + 'dm/details/v1', params=p)

def test_user_not_in_dm(clear, users):
    dm = requests.post(config.url + 'dm/create/v1', json={'token': users['tokens'][1], 'u_ids': users['u_ids'][1:]})
    dm = dm.json()
    p = {'token' : users['tokens'][0], 'dm_id' : dm['dm_id']}
    with pytest.raises(AccessError):
        requests.get(config.url + 'dm/details/v1', params=p)

def test_invalid_dm_id(clear, users):
    p = {'token' : users['tokens'][0], 'dm_id' : 'dm_id'}
    with pytest.raises(AccessError):
        requests.get(config.url + 'dm/details/v1', params=p)

def test_user_in_dm(clear, users):
    dm = requests.post(config.url + 'dm/create/v1', json={'token': users['tokens'][0], 'u_ids': users['u_ids']})
    dm = dm.json()
    p = {'token' : users['tokens'][0], 'dm_id' : dm['dm_id']}
    details = requests.get(config.url + 'dm/details/v1', params=p)
    assert len(details.json()) == 2