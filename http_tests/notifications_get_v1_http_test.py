import pytest
from src import config
import requests

@pytest.fixture
def token():
    email = "test@unsw.au"
    password = "testPassword"
    firstname = "firstName"
    lastname = "lastName"
    response = requests.post(config.url + '/auth/register/v2', json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return response.json()['token']

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

@pytest.fixture
def channel_id(token):
    channel_id = requests.post(config.url + '/channels/create/v2', json={'token': token, 'name': 'channel01', 'is_public': True})
    return channel_id.json()['channel_id']


def test_invalid_token(clear):
    response = requests.get(config.url + '/notifications/get/v1', params={'token': {'test' : 'value'}})
    assert response.status_code == 403

def return_empty_notifications(clear, token):
    notifications = requests.get(config.url + '/notifications/get/v1', params={'token' : token})
    assert notifications.json() == {'notifications' : []}

def test_return_single_notification(clear, token, channel_id):
    requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': "Test message @firstNamelastName"})
    notifications = requests.get(config.url + '/notifications/get/v1', params={'token': token})
    assert len(notifications.json()['notifications']) == 1

def test_return_correct_notification_types(clear, token, channel_id):
    requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': "Test message @firstNamelastName"})
    notifications = requests.get(config.url + '/notifications/get/v1', params={'token': token}).json()
    assert 'channel_id' in notifications['notifications'][0]
    assert 'dm_id' in notifications['notifications'][0]
    assert 'notification_message' in notifications['notifications'][0]

def test_multiple_tagged_only_1_valid(clear, token, channel_id):
    requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': "Test message @firstNamelastName and @nothername and yet @anotherTestName"})
    notifications = requests.get(config.url + '/notifications/get/v1', params={'token': token})
    assert len(notifications.json()['notifications']) == 1

def test_return_no_more_than_20_notifications(clear, token, channel_id):
    for i in range(0, 30):
        requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': f"Test {i} message @firstNamelastName"})
    notifications = requests.get(config.url + '/notifications/get/v1', params={'token': token}).json()
    assert len(notifications['notifications']) == 20
