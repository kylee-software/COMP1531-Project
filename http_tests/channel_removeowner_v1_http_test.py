import pytest
import requests
from src import config

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1').json()

@pytest.fixture
def owner():
    email = "testmail1@gamil.com"
    password = "Testpass12345"
    first_name = "firstone"
    last_name = "lastone"
    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    return user_info

@pytest.fixture
def member():
    email = "testmail2@gamil.com"
    password = "Testpass123456"
    first_name = "firsttwo"
    last_name = "lasttwo"
    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    return user_info

@pytest.fixture
def channel_id_1(owner, member):
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': "channelName1",
        'is_public': True
    }).json()['channel_id']

    requests.post(config.url + 'channel/join/v2', json={
        'token': member['token'],
        'channel_id': channel_id
    })
    return channel_id

def test_invalid_token(clear, channel_id, member):
    status_code = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': "invalid_token",
        'channel_id': channel_id,
        'u_id': member['auth_user_id']
    }).status_code

    assert status_code == 403

def test_invalid_channel_id(clear, owner, channel_id, member):
    status_code = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel_id + 1,
        'u_id': member['auth_user_id']
    }).status_code

    assert status_code == 400

def test_user_not_owner(clear, owner, channel_id):
    status_code = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'u_id': 5
    }).status_code

    assert status_code == 400

def test_remove_owner(clear, owner, channel_id):
    status_code = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'u_id': owner['auth_user_id']
    }).status_code

    assert status_code == 403

