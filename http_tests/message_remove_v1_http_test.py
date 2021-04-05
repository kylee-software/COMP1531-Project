import pytest
import requests
import json
from src import config

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1').json()

@pytest.fixture
def auth_user():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    token = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['token']
    return token

@pytest.fixture
def member():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firstone"
    last_name = "lastone"
    member = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    return member

@pytest.fixture
def channel_id(auth_user, member):
    channel_id = requests.post(config.url + '/channels/create/v2', json={
        'token': auth_user,
        'name': "channelName1",
        'is_public': True
    }).json()['channel_id']

    requests.post(config.url + 'channel/join/v2', json={'token': auth_user,
                                                        'channel_id': channel_id})
    return channel_id

@pytest.fixture
def dm_id(auth_user, member):
    dm_id = requests.post(config.url + 'dm/create/v1', json={'token': auth_user,
                                                             'u_ids': [member['auth_user_id']]
                                                             }).json()['dm_id']
    return dm_id

def test_remove_channel_message(clear, auth_user, channel_id):
    message_id = requests.post(config.url + '/message/send/v2',json={'token': auth_user,
                                                                     'channel_id': channel_id,
                                                                     'message': 'Hi'})

    response = requests.delete(config.url + 'message/remove/v1', json={'token': auth_user,
                                                                       'message_id': message_id})
    assert json.loads(response.text) == {}

def test_remove_dm_message(clear, auth_user, dm_id):
    message_id = requests.post(config.url + '/message/senddm/v1',
                               json={'token': auth_user,
                                     'dm_id': dm_id,
                                     'message': 'Hi'})

    response = requests.delete(config.url + 'message/remove/v1',
                               json={'token': auth_user,
                                     'message_id': message_id})
    assert json.loads(response.text) == {}


def test_invalid_token(clear):
    response = requests.delete(config.url + 'message/remove/v1', json={'token': "invalid_token", 'message_id': 1})
    assert response.status_code == 403

def test_unauthorised_auth_user(clear, auth_user, member, channel_id, dm_id):
    channel_message_id = requests.post(config.url + '/message/send/v2',
                                       json={'token': auth_user,
                                             'channel_id': channel_id,
                                             'message': 'Hi'})

    dm_message_id = requests.post(config.url + '/message/senddm/v1',
                                  json={'token': auth_user,
                                        'dm_id': dm_id,
                                        'message': 'Hi'}).json()['message_id']

    response1 = requests.delete(config.url + 'message/remove/v1',
                                json={'token': member['token'], 'message_id': channel_message_id})
    response2 = requests.delete(config.url + 'message/remove/v1',
                                json={'token': member['token'], 'message_id': dm_message_id})
    assert response1.status_code == 403
    assert response2.status_code == 403

def test_invalid_message_id(clear, auth_user):
    response = requests.delete(config.url + 'message/remove/v1',
                               json={'token': auth_user, 'message_id': 1})
    assert response.status_code == 400
