import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channel import channel_invite_v1
from src.channels import channels_create_v2
from src.message import message_send_v2
from src.dm import dm_create_v1

@pytest.fixture
def user1():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user2():
    email = "testemail2@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def creator():
    email = "channelcreator@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def OGchannel():
    name = "OGchannel"
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")

    channel_id = channels_create_v2(owner['token'], name, True)['channel_id']
    channel_invite_v1(owner['token'], channel_id, user1['auth_user_id'])
    return channel_id

@pytest.fixture
def share_channel():
    name = "Sharechannel"
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")
    channel_id = channels_create_v2(owner['token'], name, True)['channel_id']
    channel_invite_v1(owner['token'], channel_id, user1['auth_user_id'])
    return channel_id

@pytest.fixture
def dm():
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")
    return dm_create_v1(owner['token'], [user1['auth_user_id']])

@pytest.fixture
def clear():
    clear_v1()

def test_message_share_to_channel(clear, creator, user1, OGchannel, share_channel):
    '''
    A simple test to test the http wrapper of sharing a message to a channel
    '''
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id':OGmessage, 'message':'additional message','channel_id':share_channel, 'dm_id':-1})
    assert isinstance(resp.json()['message_id'], int)

def test_message_share_to_dm(clear, creator, user1, OGchannel, dm):
    '''
    A simple test to test the http wrapper of sharing a message to a dm
    '''
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id':OGmessage, 'message':'additional message','channel_id':-1, 'dm_id':dm['dm_id']})
    assert isinstance(resp.json()['message_id'], int)

def test_message_share_access_error(clear, creator, user1, OGchannel, share_channel):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")
    resp = requests.post(config.url + 'message/share/v1', json={'token': 'bad.token.input', 'og_message_id':OGmessage, 'message':'additional message','channel_id':share_channel, 'dm_id':-1})
    assert resp.status_code == 403

def test_message_share_input_error(clear, creator, user1, OGchannel, share_channel):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id':OGmessage, 'message':'additional message','channel_id':-1, 'dm_id':-1})
    assert resp.status_code == 400
