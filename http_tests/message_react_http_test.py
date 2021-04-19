import pytest, requests, json
from src import config

@pytest.fixture
def owner():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    token = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['token']
    return token

@pytest.fixture
def member():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "memberfirst"
    last_name = "memberlast"
    member_info = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    return member_info

@pytest.fixture
def channel_message_id(owner, member):
    channel_id = requests.post(config.url + '/channels/create/v2', json={
        'token': owner,
        'name': "channelName1",
        'is_public': True
    }).json()['channel_id']

    requests.post(config.url + 'channel/join/v2', json={'token': member['token'],
                                                        'channel_id': channel_id})

    message_id = requests.post(config.url + '/message/send/v2', json={
        'token': owner,
        'channel_id': channel_id,
        'message': 'Hi'
    }).json()['message_id']

    return message_id

@pytest.fixture
def dm_message_id(owner, member):
    dm_id = requests.post(config.url + 'dm/create/v1', json={
        'token': owner,
        'u_ids': [member['auth_user_id']]
    }).json()['dm_id']

    message_id = requests.post(config.url + '/message/senddm/v1', json={
        'token': member['token'],
        'dm_id': dm_id,
        'message': 'Hi'
    }).json()['message_id']

    return message_id

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1').json()


def test_invalid_token(clear, dm_message_id):
    status_code = requests.post(config.url + 'message/react/v1', json={
        'token': "invalid_token",
        'message_id': dm_message_id,
        'react_id': 1
    }).status_code

    assert status_code == 403

def test_user_not_a_member(clear, channel_message_id, dm_message_id):
    non_member = requests.post(config.url + 'auth/register/v2', json={
        'email': "testmail2@gmail.com",
        'password': "testpassword",
        'name_first': "nota",
        'name_last': "member"
    }).json()['token']

    channel_status_code = requests.post(config.url + 'message/react/v1', json={
        'token': non_member,
        'message_id': channel_message_id,
        'react_id': 1
    }).status_code

    dm_status_code = requests.post(config.url + 'message/react/v1', json={
        'token': non_member,
        'message_id': dm_message_id,
        'react_id': 1
    }).status_code

    assert channel_status_code == 403
    assert dm_status_code == 403

def test_invalid_message_id(clear, owner, channel_message_id, dm_message_id):
    channel_status_code = requests.post(config.url + 'message/react/v1', json={
        'token': owner,
        'message_id': channel_message_id + 2,
        'react_id': 1
    }).status_code

    dm_status_code = requests.post(config.url + 'message/react/v1', json={
        'token': owner,
        'message_id': dm_message_id + 1,
        'react_id': 1
    }).status_code

    assert channel_status_code == 400
    assert dm_status_code == 400

def test_invalid_react_id(clear, owner, channel_message_id, dm_message_id):
    channel_status_code = requests.post(config.url + 'message/react/v1', json={
        'token': owner,
        'message_id': channel_message_id,
        'react_id': 0
    }).status_code

    assert channel_status_code == 400

def test_react_twice_channel(clear, member, channel_message_id):
    requests.post(config.url + 'message/react/v1',
                 json={'token': member['token'], 'message_id': channel_message_id, 'react_id': 1})

    channel_status_code = requests.post(config.url + 'message/react/v1',
                 json={'token': member['token'], 'message_id': channel_message_id, 'react_id': 1}).status_code

    assert channel_status_code == 400

def test_react_twice_dm(clear, owner, dm_message_id):
    requests.post(config.url + 'message/react/v1',
                 json={'token': owner, 'message_id': dm_message_id, 'react_id': 1})

    dm_status_code = requests.post(config.url + 'message/react/v1',
                 json={'token': owner, 'message_id': dm_message_id, 'react_id': 1}).status_code

    assert dm_status_code == 400

def test_message_react(clear, owner, member, channel_message_id, dm_message_id):
    requests.post(config.url + 'message/react/v1', json={
        'token': owner,
        'message_id': channel_message_id,
        'react_id': 1}).json()
    requests.post(config.url + 'message/react/v1', json={
        'token': owner,
        'message_id': dm_message_id,
        'react_id': 1}).json()

    channel_resp = requests.post(config.url + 'message/react/v1', json={
        'token': member['token'],
        'message_id': channel_message_id,
        'react_id': 1}).json()
    dm_resp = requests.post(config.url + 'message/react/v1', json={
        'token': member['token'],
        'message_id': dm_message_id,
        'react_id': 1}).json()

    assert channel_resp == {}
    assert dm_resp == {}