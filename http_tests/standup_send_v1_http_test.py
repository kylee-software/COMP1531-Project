import pytest
import requests
import time
from src import config
import random
import string

@pytest.fixture
def token():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    auth_resp = requests.post(config.url + '/auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    })
    return auth_resp.json()['token']
    

@pytest.fixture
def channel_id(token):
    return requests.post(config.url + 'channels/create/v2', json={
        'token': token,
        'name': "testChannel",
        'is_public': True
    }).json()['channel_id']

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

def test_invalid_token(clear, channel_id):
    response = requests.post(config.url + 'standup/send/v1', json={'token': 'invalid_token', 'channel_id': channel_id, 'message' : 'Hello There'})
    assert response.status_code == 403

def test_invalid_channel_id(clear, token):
    response = requests.post(config.url + 'standup/send/v1', json={'token': token, 'channel_id': 'invalid_channel_id', 'message' : 'Hello There'})
    assert response.status_code == 400

def test_message_more_than_1000(clear, token, channel_id):
    message = ''.join(random.choices(string.ascii_letters, k = 1001))
    requests.post(config.url + 'standup/start/v1', json={'token': token, 'channel_id': channel_id, 'length' : 1})
    response = requests.post(config.url + 'standup/send/v1', json={'token': token, 'channel_id': channel_id, 'message' : message})
    assert response.status_code == 400

def test_no_active_standup(clear, token, channel_id):
    response = requests.post(config.url + 'standup/send/v1', json={'token': token, 'channel_id': channel_id, 'message' : 'Hello There'})
    assert response.status_code == 400

def test_user_not_in_channel(clear, token, channel_id):
    token2 = requests.post(config.url + '/auth/register/v2', json={
        'email': 'testing@gmail.com',
        'password': 'password',
        'name_first': 'first_name',
        'name_last': 'last_name'
    }).json()['token']
    requests.post(config.url + 'standup/start/v1', json={'token': token, 'channel_id': channel_id, 'length' : 1})
    response = requests.post(config.url + 'standup/send/v1', json={'token': token2, 'channel_id': channel_id, 'message' : 'Hello There'})
    assert response.status_code == 403

def test_all_working(clear, token, channel_id):
    requests.post(config.url + 'standup/start/v1', json={'token': token, 'channel_id': channel_id, 'length' : 1})
    response = requests.post(config.url + 'standup/send/v1', json={'token': token, 'channel_id': channel_id, 'message' : 'Hello There'})
    assert response.status_code == 200