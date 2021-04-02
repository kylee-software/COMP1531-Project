import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channel import channel_join_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError


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

@pytest.fixture
def dm(user2, user3):
    return dm_create_v1(user2['token'], [user3['auth_user_id']])

@pytest.fixture
def clear():
    clear_v1()



def test_message_senddm(clear, dm):
    '''
    A simple test to check message send dm
    '''
    user2 = auth_login_v2("test2email@gmail.com", "TestTest2")
    resp = requests.post(config.url + 'message/senddm/v1', json={'token': user2['token'], 'dm_id':dm['dm_id'], 'message':'messagemessage'})
    assert resp.status_code == 200
    assert isinstance(json.loads(resp.text), int)

def test_message_senddm_access(clear, dm, user1):
    '''
    A simple test to check message send dm access error
    '''
    resp = requests.post(config.url + 'message/senddm/v1', json={'token': user1['token'], 'dm_id':dm['dm_id'], 'message':'messagemessage'})
    assert resp.status_code == 400

def test_message_senddm_input(clear, dm):
    '''
    A simple test to check message send dm input error
    '''
    user2 = auth_login_v2("test2email@gmail.com", "TestTest2")
    resp = requests.post(config.url + 'message/senddm/v1', json={'token': user2['token'], 'dm_id':dm['dm_id'], 'message':'messagelong'*500})
    assert resp.status_code == 200
