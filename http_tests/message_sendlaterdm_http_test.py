import pytest
import requests
from src import config
from datetime import datetime, timezone
import random, string

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

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
    }).json()
    token = auth_resp['token']
    return token

@pytest.fixture
def dm_id(token):
    member = requests.post(config.url + 'auth/register/v2', json={
        'email': "testmail1@gamil.com",
        'password': "Testpass123456",
        'name_first': "firstone",
        'name_last': "lastone"
    }).json()['auth_user_id']

    dm_id = requests.post(config.url + 'dm/create/v1', json={
        'token': token,
        'u_ids': [member]
    }).json()['dm_id']

    return dm_id

@pytest.fixture
def timestamp():
    return datetime.now().replace(tzinfo=timezone.utc).timestamp()

def test_invalid_token(clear, token, dm_id, timestamp):
    status_code = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': "invalid_token",
        'dm_id': dm_id,
        'message': "Hi",
        'time_sent': timestamp
    }).status_code
    assert status_code == 403

def test_invalid_dm_id(clear, token, dm_id, timestamp):
    status_code = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': token,
        'dm_id': dm_id + 1,
        'message': "Hi",
        'time_sent': timestamp
    }).status_code
    assert status_code == 400

def test_user_not_in_channel(clear, token, dm_id, timestamp):
    not_member_token = requests.post(config.url + 'auth/register/v2', json={
        'email': 'test2@unsw.au',
        'password': 'testPassword',
        'name_first': 'secondFirst',
        'name_last': 'secondLast'}).json()['token']

    status_code = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': not_member_token,
        'dm_id': dm_id,
        'message': "Hi",
        'time_sent': timestamp
    }).status_code
    assert status_code == 403

def test_message_too_long(clear, token, dm_id, timestamp):
    message = ''.join(random.choices(string.ascii_letters, k=1001))
    status_code = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': token,
        'dm_id': dm_id,
        'message': message,
        'time_sent': timestamp
    }).status_code
    assert status_code == 400

def test_invalid_time_sent(clear, token, dm_id, timestamp):
    status_code = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': token,
        'dm_id': dm_id,
        'message': "Hi",
        'time_sent': timestamp - 2.0
    }).status_code
    assert status_code == 400

def test_message_send_later(clear, token, dm_id, timestamp):
    message_id = requests.post(config.url + 'message/sendlaterdm/v1', json={
        'token': token,
        'dm_id': dm_id,
        'message': "Hi",
        'time_sent': timestamp + 2.0
    }).json()['message_id']
    assert message_id == 1
