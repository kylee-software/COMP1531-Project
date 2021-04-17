import requests
import pytest
from src import config


@pytest.fixture(autouse=True)
def clear():
    requests.delete(config.url + '/clear/v1')


@pytest.fixture
def create_admin():
    admin = requests.post(config.url + '/auth/register/v2',
                          json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'first', 'name_last': 'last'})
    admin_details = admin.json()
    return admin_details


@pytest.fixture
def create_member_1():
    member = requests.post(config.url + '/auth/register/v2',
                           json={'email': 'test1@unsw.au', 'password': 'password1', 'name_first': 'test1', 'name_last': 'last1'})
    member_1_details = member.json()
    return member_1_details


@pytest.fixture
def channel(create_admin):
    return requests.post(config.url + '/channels/create/v2', json={'token': create_admin['token'], 'name': 'channel_1', 'is_public': True}).json()


@ pytest.fixture
def dm(create_admin, create_member_1):
    return requests.post(config.url + '/dm/create/v1', json={'token': create_admin['token'], 'u_ids': [create_member_1['auth_user_id']]}).json()


@ pytest.fixture
def channel_message(create_admin, channel):
    return requests.post(config.url + '/message/send/v2', json={'token': create_admin['token'], 'channel_id': channel['channel_id'], 'message': 'this is a message sent to the other user in the channel.'}).json()


@ pytest.fixture
def dm_message(create_admin, dm):
    return requests.post(config.url + '/message/senddm/v1', json={'token': create_admin['token'], 'dm_id': dm['dm_id'], 'message': 'this is a message sent to the other user.'}).json()


@pytest.fixture
def not_member():
    not_a_member = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'notmember@unsw.au', 'password': 'password123', 'name_first': 'notmemberfirst', 'name_last': 'notmemberlast'})
    not_member_details = not_a_member.json()
    return not_member_details


def test_invalid_message_id(clear, create_admin, channel_message):
    result = requests.post(config.url + '/message/pin/v1', json={
                           'token': create_admin['token'], 'message_id': 123456})
    assert result.status_code == 400


def test_message_already_pinned_channel(clear, create_admin, channel_message):
    requests.post(config.url + '/message/pin/v1', json={
                  'token': create_admin['token'], 'message_id': channel_message['message_id']})
    result = requests.post(config.url + '/message/pin/v1', json={
                           'token': create_admin['token'], 'message_id': channel_message['message_id']})
    assert result.status_code == 400


def test_message_already_pinned_dm(clear, create_admin, dm_message):
    requests.post(config.url + '/message/pin/v1',
                  json={'token': create_admin['token'], 'message_id': dm_message['message_id']})
    result = requests.post(config.url + '/message/pin/v1', json={
                           'token': create_admin['token'], 'message_id': dm_message['message_id']})
    assert result.status_code == 400


def test_user_not_member_channel(clear, channel_message, create_admin, not_member):
    result = requests.post(config.url + '/message/pin/v1', json={
                           'token': not_member['token'], 'message_id': channel_message['message_id']})
    assert result.status_code == 403


def test_user_not_member_dm(clear, dm_message, create_admin, not_member):
    result = requests.post(config.url + '/message/pin/v1', json={
                           'token': not_member['token'], 'message_id': dm_message['message_id']})
    assert result.status_code == 403


def test_not_channel_owner(clear, create_admin, create_member_1, channel_message):
    result = requests.post(config.url + '/message/pin/v1', json={
                           'token': create_member_1['token'], 'message_id': channel_message['message_id']})
    assert result.status_code == 403


def test_not_dm_owner(clear, create_admin, create_member_1, dm_message):
    result = requests.post(config.url + '/message/pin/v1', json={
                           'token': create_member_1['token'], 'message_id': dm_message['message_id']})
    assert result.status_code == 403


def test_success_case_channel(clear, create_admin, create_member_1, channel, channel_message):
    requests.post(config.url + '/message/pin/v1', json={
                  'token': create_admin['token'], 'message_id': channel_message['message_id']})
    channel_message_dict = requests.get(config.url + '/channel/messages/v2', params={
                                        'token': create_admin['token'], 'channel_id': channel['channel_id'], 'start': 0})
    channel_messages = channel_message_dict.json()
    assert channel_messages['messages'][0]['is_pinned'] == True


def test_success_case_dm(clear, create_admin, create_member_1, dm, dm_message):
    requests.post(config.url + '/message/pin/v1', json={
                  'token': create_admin['token'], 'message_id': dm_message['message_id']})
    dm_message_dict = requests.get(config.url + '/dm/messages/v1', params={
        'token': create_admin['token'], 'dm_id': dm['dm_id'], 'start': 0})
    dm_messages = dm_message_dict.json()
    assert dm_messages['messages'][0]['is_pinned'] == True
