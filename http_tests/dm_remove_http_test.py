import pytest
import requests
import json
from src import config


@pytest.fixture
def user0():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)


@pytest.fixture
def owner():
    email = "dmcreator@gmail.com"
    password = "TestTest1"
    firstname = "first"
    lastname = "last"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)

@pytest.fixture
def dm(owner, user0):
    dm = requests.post(config.url + '/dm/create/v1',
                        json={'token':owner['token'], 'u_ids':[user0['auth_user_id']]})
    return json.loads(dm.text)

@pytest.fixture
def owner_token():
    owner = requests.post(config.url + '/auth/login/v2',
                        json={'email': "dmcreator@gmail.com", 'password': "TestTest1"})
    return json.loads(owner.text)['token']


@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

def test_dm_remove(clear, dm, owner_token):
    resp = requests.delete(config.url + 'dm/remove/v1', json={'token': owner_token, 'dm_id':dm['dm_id']})
    assert resp.json() == {}

def test_dm_remove_access_error(clear, dm, owner_token):
    resp = requests.delete(config.url + 'dm/remove/v1', json={'token': 'bad.token.input', 'dm_id':dm['dm_id']})
    assert resp.status_code == 403

def test_dm_remove_input_error(clear, dm, owner_token):
    resp = requests.delete(config.url + 'dm/remove/v1', json={'token': owner_token, 'dm_id':dm['dm_id'] + 1})
    assert resp.status_code == 400