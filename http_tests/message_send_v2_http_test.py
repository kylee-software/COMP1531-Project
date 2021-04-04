import pytest
import requests
from src import config
import random
import string

@pytest.fixture
def token():
    email = "test@unsw.au"
    password = "testPassword"
    firstname = "firstName"
    lastname = "lastName"
    response = requests.post(config.url + '/auth/register/v2', json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return response.json()['token']

@pytest.fixture
def channel_id(token):
    response = requests.post(config.url + '/channels/create/v2', json={'token': token, 'name': 'testChannel01', 'is_public': False})
    return response.json()['channel_id']

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')


def test_message_too_long(clear, token, channel_id):
    message = ''.join(random.choices(string.ascii_letters, k = 1001))
    response = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': message})
    assert response.status_code == 400

def test_invalid_token(clear, token, channel_id):
    response = requests.post(config.url + '/message/send/v2', json={'token': 'invalid_token', 'channel_id': channel_id, 'message': 'test_message'})
    assert response.status_code == 403

def test_user_not_in_channel(clear, token, channel_id):
    second_token = requests.post(config.url + 'auth/register/v2', json={'email': 'test2@unsw.au', 'password': 'testPassword', 'name_first': 'secondFirst', 'name_last': 'secondLast'})
    second_token = second_token.json()['token']
    response = requests.post(config.url + '/message/send/v2', json={'token': second_token, 'channel_id': channel_id, 'message': 'test_message'})
    assert response.status_code == 403

def test_message_ids_are_unique(clear, token, channel_id):
    m_id1 = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': 'test_message'})
    m_id2 = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': 'test_message'})
    m_id1 = m_id1.json()
    m_id2 = m_id2.json()
    assert m_id1 != m_id2

def test_message_with_notification(clear, token, channel_id):
    m_id = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': 'test message @firstNamelastName'})
    m_id = m_id.json()
    assert isinstance(m_id, int)

def test_invalid_channel_id(clear, token):
    response = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': 'channel_id', 'message': 'test message'})
    assert response.status_code == 400