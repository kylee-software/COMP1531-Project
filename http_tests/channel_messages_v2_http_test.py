import pytest
import requests
from src import config
from src.helper import load_data


# @pytest.fixture
# def clear():
#     requests.delete(config.url + '/clear/v1')

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
def channel_id(token):
    resp = requests.post(config.url + '/channels/create/v2', json={
        'token': token,
        'name': "channelName1",
        'is_public': True
    }).json()

    channel_id = resp['channel_id']
    return channel_id

def test_invalid_token(clear, channel_id):
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': "invalid_token",
        'channel_id': channel_id,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 403

def test_invalid_channel_id(clear, token, channel_id):
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id + 1,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 400

def test_user_not_in_channel(clear, channel_id):
    not_member_token = requests.post(config.url + 'auth/register/v2', json={
        'email': 'test2@unsw.au',
        'password': 'testPassword',
        'name_first': 'secondFirst',
        'name_last': 'secondLast'})
    not_member_token = not_member_token.json()['token']

    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': not_member_token,
        'channel_id': channel_id,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 403

def test_invalid_start(clear, token, channel_id):
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id,
        'start': 51
    })
    print(resp)

    status_code = resp.status_code
    assert status_code == 400

def test_messages(clear, token, channel_id):
    for i in range(3):
        requests.post(config.url + '/message/send/v2', json={
            'token': token,
            'channel_id': channel_id,
            'message': f"{i}"
        })

    messages_dict = requests.get(config.url + '/channel/messages/v2', params={
            'token': token,
            'channel_id': channel_id,
            'start': 0
        }).json()

    assert messages_dict['messages'][0]['message'] == '2'

