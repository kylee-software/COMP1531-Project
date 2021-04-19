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
    response = requests.post(config.url + 'standup/start/v1', json={'token': 'invalid_token', 'channel_id': channel_id, 'length' : 1})
    assert response.status_code == 403

def test_invalid_channel_id(clear, token):
    response = requests.post(config.url + 'standup/start/v1', json={'token': token, 'invalid_channel_id': channel_id, 'length' : 1})
    assert response.status_code == 400

def test_standup_already_running(clear, token, channel_id):
    requests.post(config.url + 'standup/start/v1', json={'token': token, 'channel_id': channel_id, 'length' : 1})
    response = requests.post(config.url + 'standup/start/v1', json={'token': token, 'channel_id': channel_id, 'length' : 1})
    assert response.status_code == 400

def test_user_not_in_channel(clear, channel_id):
    invalid_token = requests.post(config.url + '/auth/register/v2', json={
        'email': 'test342@gmail.com',
        'password': 'password',
        'name_first': 'first_name',
        'name_last': 'last_name'
    }).json()['token']
    response = requests.post(config.url + 'standup/start/v1', json={'token': invalid_token, 'channel_id': channel_id, 'length' : 1})
    assert response.status_code == 403

def test_standup_works(clear, token, channel_id):
    requests.post(config.url + 'standup/start/v1', json={'token': token, 'channel_id': channel_id, 'length' : 1})
    response = requests.get(config.url + 'standup/active/v1', params={'token' : token, 'channel_id': channel_id})
    assert response.json()['is_active'] == True

def test_standup_ends(clear, token, channel_id):
    requests.post(config.url + 'standup/start/v1', json={'token': token, 'channel_id': channel_id, 'length' : 1})
    response = requests.get(config.url + 'standup/active/v1', params={'token' : token, 'channel_id': channel_id})
    assert response.json()['is_active'] == True

    time.sleep(3)
    response = requests.get(config.url + 'standup/active/v1', params={'token' : token, 'channel_id': channel_id})
    assert response.json()['is_active'] == False