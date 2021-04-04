import pytest
import requests
from src import config


@pytest.fixture
def token():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    auth_resp = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    token = auth_resp['token']
    print(token)
    return token

@pytest.fixture
def channel_id(token):
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': token,
        'name': "channelName1",
        'is_public': True
    }).json()

    channel_id = resp['channel_id']
    return channel_id

@pytest.fixture
def unauthorised_user():
    email = "testmail2@gamil.com"
    password = "Testpass1234567"
    first_name = "first"
    last_name = "last"
    auth_resp = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    token = auth_resp['token']
    return token

def test_invalid_token(channel_id):
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': "invalid_token",
        'channel_id': channel_id,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 403

def test_invalid_channel_id(token, channel_id):
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id + 1,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 400

def test_unauthorised_user(unauthorised_user, channel_id):
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': unauthorised_user,
        'channel_id': channel_id,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 403

def test_invalid_start(token, channel_id):
    resp = requests.get(config.url + 'channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id,
        'start': 51
    })

    status_code = resp.status_code
    assert status_code == 400

def test_last_message(token, channel_id):
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': token,
        'channel_id': channel_id,
        'message': "Hi, everyone!"
    }).json()
    end = resp['end']
    assert end == -1

def test_more_messages(token, channel_id):
    count = 60
    while count >= 0:
        requests.post(config.url + 'message/send/v2', json={
            'token': token,
            'channel_id': channel_id,
            'message': f"{count}"
        })
        count -= 1

    # Test first 50 newest messages
    resp_1 = requests.get(config.url + 'channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id,
        'start': 0
    }).json()
    message_1 = resp_1['messages'][49]['message']
    assert message_1 == '49'

    # Test the first message in the returned message dictionary
    resp_2 = requests.get(config.url + 'channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id,
        'start': 10
    }).json()
    message_2 = resp_2['messages'][0]['message']
    assert message_2 == '10'

    # Test the second message in the returned message dictionary
    resp_3 = requests.get(config.url + 'channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id,
        'start': 30
    }).json()
    message_3 = resp_3['messages'][1]['message']
    assert message_3 == '31'

    # Test the earliest message that was sent to the channel
    resp_4 = requests.get(config.url + 'channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id,
        'start': 60
    }).json()
    message_4 = resp_4['messages'][0]['message']
    assert message_4 == '60'

    requests.delete(config.url + 'clear/v1')
