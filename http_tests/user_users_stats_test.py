import pytest
import requests
import json
from src import config

ACCESS_ERROR_CODE = 403
INPUT_ERROR_CODE = 400

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
def creator():
    email = "channelcreator@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)

@pytest.fixture
def channel():
    channel_name = "OGchannel"
    owner = requests.post(config.url + '/auth/login/v2',
                                 json={'email': "channelcreator@gmail.com", 'password': "TestTest2"})
    owner = json.loads(owner.text)
    channel_id = requests.post(config.url + 'channels/create/v2', json={
                                'token': owner['token'],
                                'name': channel_name,
                                'is_public': True
                                })
    channel_id = json.loads(channel_id.text)['channel_id']

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

def test_user_stats_valid(clear, creator, user1, channel, dm):
    '''
    A simple test to check user stats
    '''
    requests.post(config.url + '/message/send/v2',
        json={'token':creator['token'], 'channel_id':channel, 'message':"TestMessage"})

    resp = requests.get(config.url + 'user/stats/v1', params={'token': creator['token']})
    resp = json.loads(resp.text)
    assert len(resp['channels_joined']) == 1
    assert len(resp['dms_joined']) == 1
    assert len(resp['messages_sent']) == 1
    assert resp['involvement_rate'] == 1

def test_user_stats_access_error(clear, creator, channel):
    resp = requests.get(config.url + 'user/stats/v1', params={'token': 'bad.token.input'})
    assert resp.status_code == ACCESS_ERROR_CODE


### TEST USERS STATS (DREAMS STATS) ###
def test_users_stats_valid(clear, creator, user1, channel, dm):
    '''
    A simple test to check user stats
    '''
    requests.post(config.url + '/message/send/v2',
        json={'token':creator['token'], 'channel_id':channel, 'message':"TestMessage"})

    resp = requests.get(config.url + 'users/stats/v1', params={'token': creator['token']})
    resp = json.loads(resp.text)
    assert len(resp['channels_exist']) == 1
    assert len(resp['dms_exist']) == 1
    assert len(resp['messages_exist']) == 1
    assert resp['utilization_rate'] == 1

def test_users_stats_access_error(clear, creator, channel):
    resp = requests.get(config.url + 'users/stats/v1', params={'token': 'bad.token.input'})
    assert resp.status_code == ACCESS_ERROR_CODE
