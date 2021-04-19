import pytest
import requests
import time
from src import config

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
    response = requests.get(config.url + 'standup/active/v1', params={'token' : 'invalid_token', 'channel_id': channel_id})
    assert response.status_code == 403

def test_invalid_channel_id(clear, token):
    response = requests.get(config.url + 'standup/active/v1', params={'token' : token, 'channel_id': 'invalid_channel_id'})
    assert response.status_code == 400

def test_standup_running_returns_true(clear, token, channel_id):
    requests.post(config.url + 'standup/start/v1', json={'token': token, 'channel_id': channel_id, 'length' : 1})
    response = requests.get(config.url + 'standup/active/v1', params={'token' : token, 'channel_id': channel_id})
    assert response.json()['is_active'] == True

def test_returns_false(clear, token, channel_id):
    response = requests.get(config.url + 'standup/active/v1', params={'token' : token, 'channel_id': channel_id})
    assert response.json()['is_active'] == False
    response = requests.get(config.url + 'standup/active/v1', params={'token' : token, 'channel_id': channel_id})
    assert response.json()['time_finish'] == None