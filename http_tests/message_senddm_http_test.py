import pytest
import requests
import json
from src import config

@pytest.fixture
def user1():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)

@pytest.fixture
def user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)

@pytest.fixture
def user3():
    email = "test3email@gmail.com"
    password = "TestTest3"
    firstname = "firstname3"
    lastname = "lastname3"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)

@pytest.fixture
def dm(user2, user3):
    dm = requests.post(config.url + '/dm/create/v1',
                        json={'token':user2['token'], 'u_ids':[user3['auth_user_id']]})

    return json.loads(dm.text)

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')




def test_message_senddm(clear, dm):
    '''
    A simple test to check message send dm
    '''
    user2 = requests.post(config.url + '/auth/login/v2',
                        json={'email': "test2email@gmail.com", 'password': "TestTest2"})
    user2 = json.loads(user2.text)
    resp = requests.post(config.url + 'message/senddm/v1', json={'token': user2['token'], 'dm_id':dm['dm_id'], 'message':'messagemessage'})
    assert isinstance(resp.json()['message_id'], int)

def test_message_senddm_access(clear, dm, user1):
    '''
    A simple test to check message send dm access error
    '''
    resp = requests.post(config.url + 'message/senddm/v1', json={'token': user1['token'], 'dm_id':dm['dm_id'], 'message':'messagemessage'})
    assert resp.status_code == 403

def test_message_senddm_input(clear, dm):
    '''
    A simple test to check message send dm input error
    '''
    user2 = requests.post(config.url + '/auth/login/v2',
                        json={'email': "test2email@gmail.com", 'password': "TestTest2"})
    user2 = json.loads(user2.text)
    resp = requests.post(config.url + 'message/senddm/v1', json={'token': user2['token'], 'dm_id':dm['dm_id'], 'message':'messagelong'*500})
    assert resp.status_code == 400
