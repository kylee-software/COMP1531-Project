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
    email = "testemail2@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)
    
@pytest.fixture
def creator():
    email = "channelcreator@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)

@pytest.fixture
def OGchannel():
    channel_name = "OGchannel"
    owner = requests.post(config.url + '/auth/login/v2',
                                 json={'email': "channelcreator@gmail.com", 'password': "TestTest2"})
    user1 = requests.post(config.url + '/auth/login/v2',
                                 json={'email': "testemail@gmail.com", 'password': "TestTest"})
    owner = json.loads(owner.text)
    user1 = json.loads(user1.text)
    channel_id = requests.post(config.url + 'channels/create/v2', json={
                                'token': owner['token'],
                                'name': channel_name,
                                'is_public': True
                                })
    channel_id = json.loads(channel_id.text)['channel_id']
    requests.post(config.url + '/channel/invite/v2',
                json={'token': owner['token'], 'channel_id':channel_id, 'u_id':user1['auth_user_id']})
   
    return channel_id

@pytest.fixture
def share_channel():
    channel_name = "Sharechannel"
    owner = requests.post(config.url + '/auth/login/v2',
                                 json={'email': "channelcreator@gmail.com", 'password': "TestTest2"})
    user1 = requests.post(config.url + '/auth/login/v2',
                                 json={'email': "testemail@gmail.com", 'password': "TestTest"})
    owner = json.loads(owner.text)
    user1 = json.loads(user1.text)
    channel_id = requests.post(config.url + 'channels/create/v2', json={
                                'token': owner['token'],
                                'name': channel_name,
                                'is_public': True
                                })
    channel_id = json.loads(channel_id.text)['channel_id']
    requests.post(config.url + '/channel/invite/v2',
                json={'token': owner['token'], 'channel_id': channel_id, 'u_id':user1['auth_user_id']})
   
    return channel_id

@pytest.fixture
def dm():
    owner = requests.post(config.url + '/auth/login/v2',
                        json={'email': "channelcreator@gmail.com", 'password': "TestTest2"})
    user1 = requests.post(config.url + '/auth/login/v2',
                        json={'email': "testemail@gmail.com", 'password': "TestTest"})
    owner = json.loads(owner.text)
    user1 = json.loads(user1.text)
    dm = requests.post(config.url + '/dm/create/v1',
                        json={'token':owner['token'], 'u_ids':[user1['auth_user_id']]})

    return json.loads(dm.text)['dm_id']

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')


def test_message_share_to_channel(clear, creator, user1, OGchannel, share_channel):
    '''
    A simple test to test the http wrapper of sharing a message to a channel
    '''
    OGmessage = requests.post(config.url + '/message/send/v2',
                        json={'token':creator['token'], 'channel_id':OGchannel, 'message':"TestMessage"})
    OGmessage = json.loads(OGmessage.text)['message_id']
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id':OGmessage, 'message':'additional message','channel_id':share_channel, 'dm_id':-1})
    assert isinstance(resp.json()['shared_message_id'], int)

def test_message_share_to_dm(clear, creator, user1, OGchannel, dm):
    '''
    A simple test to test the http wrapper of sharing a message to a dm
    '''
    OGmessage = requests.post(config.url + '/message/send/v2',
                    json={'token':creator['token'], 'channel_id':OGchannel, 'message':"TestMessage"})
    OGmessage = json.loads(OGmessage.text)['message_id']
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id':OGmessage, 'message':'additional message','channel_id':-1, 'dm_id':dm})
    assert isinstance(resp.json()['shared_message_id'], int)

def test_message_share_access_error(clear, creator, user1, OGchannel, share_channel):
    OGmessage = requests.post(config.url + '/message/send/v2',
                        json={'token':creator['token'], 'channel_id':OGchannel, 'message':"TestMessage"})
    OGmessage = json.loads(OGmessage.text)['message_id']
    resp = requests.post(config.url + 'message/share/v1', json={'token': 'bad.token.input', 'og_message_id':OGmessage, 'message':'additional message','channel_id':share_channel, 'dm_id':-1})
    assert resp.status_code == 403

def test_message_share_input_error(clear, creator, user1, OGchannel, share_channel):
    OGmessage = requests.post(config.url + '/message/send/v2',
                        json={'token':creator['token'], 'channel_id':OGchannel, 'message':"TestMessage"})
    OGmessage = json.loads(OGmessage.text)['message_id']
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id':OGmessage, 'message':'additional message','channel_id':-1, 'dm_id':-1})
    assert resp.status_code == 400
