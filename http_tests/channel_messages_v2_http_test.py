import pytest
import requests
from src import config

def clear():
    '''
        Reset the data
    '''
    requests.delete(config.url + 'clear/v1').json()
    return

@pytest.fixture
def token():
    '''
        Create a token for the user
    '''
    clear()
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    auth_resp = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    })
    token = auth_resp.json()['token']
    return token

@pytest.fixture
def channel_id(token):
    '''
        Create a channel with "token" and return the channel_id
    '''
    resp = requests.post(config.url + 'channels/create/v2', json={
        'token': token,
        'name': "channelName1",
        'is_public': True
    })

    channel_id = resp.json()['channel_id']
    return channel_id

@pytest.fixture
def unauthorised_user():
    '''
        Create a token for an unauthorised user
    '''
    email = "testmail2@gamil.com"
    password = "Testpass1234567"
    first_name = "first"
    last_name = "last"
    auth_resp = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    })
    token = auth_resp.json()['token']
    return token

def test_invalid_token(channel_id):
    '''
        Test for invalid token
        Status code for AccessError is 403
    '''
    resp = requests.get(config.url + 'channels/messages/v2', json={
        'token': "invalid_token",
        'channel_id': channel_id,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 403

def test_invalid_channel_id(token, channel_id):
    '''
        Test for invalid channel id
        Status code for InputError is 400
    '''
    resp = requests.get(config.url + 'channels/messages/v2', json={
        'token': token,
        'channel_id': channel_id + 1,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 400

def test_unauthorised_user(unauthorised_user, channel,_id):
    '''
        Test an user that does not belong to the channel with the given channel_id
        Status code for AccessError is 403
    '''
    resp = requests.get(config.url + 'channels/messages/v2', json={
        'token': unauthorised_user,
        'channel_id': channel_id,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 403

def test_invalid_start(token, channel_id):
    '''
        Test invalid start
        Status code for InputError is 400
    '''
    resp = requests.get(config.url + 'channels/messages/v2', json={
        'token': token,
        'channel_id': channel_id,
        'start': 51
    })

    status_code = resp.status_code
    assert status_code == 400

def test_last_message(token, channel_id):
    '''
        Test if end = -1 when there are no more messages to load after the current return
    '''
    resp = requests.post(config.url + 'message/send/v2', json={
        'token': token,
        'channel_id': channel_id,
        'message': "Hi, everyone!"
    })
    end = resp.json()['end']
    assert end == -1

def test_more_messages(token, channel_id):
    clear()
    count = 60
    while count >= 0:
        requests.post(config.url + 'message/send/v2', json={
            'token': token,
            'channel_id': channel_id,
            'message': f"{count}"
        })
        count -= 1

    # Test first 50 newest messages
    resp_1 = requests.get(config.url + 'channels/messages/v2', json={
        'token': token,
        'channel_id': channel_id,
        'start': 0
    })
    message_1 = resp_1.json()['messages'][49]['message']
    assert message_1 == '49'

    # Test the first message in the returned message dictionary
    resp_2 = requests.get(config.url + 'channels/messages/v2', json={
        'token': token,
        'channel_id': channel_id,
        'start': 10
    })
    message_2 = resp_2.json()['messages'][0]['message']
    assert message_2 == '10'

    # Test the second message in the returned message dictionary
    resp_3 = requests.get(config.url + 'channels/messages/v2', json={
        'token': token,
        'channel_id': channel_id,
        'start': 30
    })
    message_3 = resp_3.json()['messages'][1]['message']
    assert message_3 == '31'

    # Test the earliest message that was sent to the channel
    resp_4 = requests.get(config.url + 'channels/messages/v2', json={
        'token': token,
        'channel_id': channel_id,
        'start': 60
    })
    message_4 = resp_4.json()['messages'][0]['message']
    assert message_4 == '60'
