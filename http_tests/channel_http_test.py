import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channel import channel_join_v1, channel_details_v1
from src.channels import channels_create_v2
from src.error import InputError, AccessError

@pytest.fixture
def user1():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)


@pytest.fixture
def channel_id():
    channel_name = "Testchannel"
    email = "channelcreator@gmail.com"
    password = "TestTest1"
    firstname = "first"
    lastname = "last"
    owner = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})

    owner = json.loads(owner.text)
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': channel_name,
        'is_public': True
    })
    
    return json.loads(channel_id.text)['channel_id']

@pytest.fixture
def channel_owner():

    owner_details = requests.post(config.url + '/auth/login/v2',
                            json={'email': "channelcreator@gmail.com", 'password': "TestTest1"})

    return json.loads(owner_details.text)

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

##### Channel Details Tests #####

def test_channel_details(clear, channel_id, channel_owner):
    '''
    A simple test to check channel details
    '''
    resp = requests.get(config.url + 'channel/details/v2', params={'token': channel_owner['token'], 'channel_id':channel_id})
    resp = resp.json()
    assert resp == {
                        'name':"Testchannel",
                        'is_public':True,
                        'owner_members':[{
                                            'u_id':channel_owner['auth_user_id'], 
                                            "email":"channelcreator@gmail.com", 
                                            'name_first':"first",
                                            'name_last':"last",
                                            'handle_str':"firstlast",
                                            },],
                        'all_members':[{
                                            'u_id':channel_owner['auth_user_id'], 
                                            "email":"channelcreator@gmail.com", 
                                            'name_first':"first",
                                            'name_last':"last",
                                            'handle_str':"firstlast",
                                        }, ],
                                        
                        }

def test_channel_details_access_error(clear, channel_id, channel_owner):
    resp = requests.get(config.url + 'channel/details/v2', params={'token': 'bad.token.input', 'channel_id':channel_id})
    assert resp.status_code == 403

def test_channel_details_input_error(clear, channel_id, channel_owner):
    resp = requests.get(config.url + 'channel/details/v2', params={'token': channel_owner['token'], 'channel_id':channel_id + 1})
    assert resp.status_code == 400


##### Channel Join Tests #####

def test_channel_join(clear, channel_id, user1):
    '''
    A simple test to check channel join
    '''
    resp = requests.post(config.url + 'channel/join/v2', json={'token': user1['token'], 'channel_id':channel_id})
    assert json.loads(resp.text) == {}

def test_channel_join_access_error(clear, channel_id, user1):
    resp = requests.post(config.url + 'channel/join/v2', json={'token': 'bad.token.input', 'channel_id':channel_id})
    assert resp.status_code == 403

def test_channel_join_input_error(clear, channel_id, user1):
    resp = requests.post(config.url + 'channel/join/v2', json={'token': user1['token'], 'channel_id':channel_id + 1})
    assert resp.status_code == 400



##### Channel Invite Tests #####

def test_channel_invite(clear, channel_id, channel_owner, user1):
    '''
    A simple test to check channel invite
    '''
    resp = requests.post(config.url + 'channel/invite/v2', json={'token': channel_owner['token'], 'channel_id':channel_id, 'u_id':user1['auth_user_id']})
    assert json.loads(resp.text) == {}
    clear_v1()

def test_channel_invite_access_error(clear, channel_id, channel_owner, user1):
    resp = requests.post(config.url + 'channel/invite/v2', json={'token': 'bad.input.token', 'channel_id':channel_id, 'u_id':user1['auth_user_id']})
    assert resp.status_code == 403

def test_channel_invite_input_error(clear, channel_id, channel_owner, user1):
    resp = requests.post(config.url + 'channel/invite/v2', json={'token': channel_owner['token'], 'channel_id':channel_id + 1, 'u_id':user1['auth_user_id']})
    assert resp.status_code == 400
    clear_v1()