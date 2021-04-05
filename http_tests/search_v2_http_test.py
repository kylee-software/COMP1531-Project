import pytest
import requests
from src import config
from src.auth import auth_register_v2, auth_login_v2
from src.error import AccessError, InputError
from src.message import message_edit_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.message import message_send_v2, message_senddm_v1
from src.channel import channel_messages_v2


@pytest.fixture(autouse=True)
def clear():
    requests.delete(config.url + '/clear/v1')
    yield
    requests.delete(config.url + '/clear/v1')


@pytest.fixture
def admin():
    admin = requests.post(config.url + '/auth/register/v2',
                          json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'first', 'name_last': 'last'})
    admin_details = admin.json()
    return admin_details


@pytest.fixture
def member():
    member = requests.post(config.url + '/auth/register/v2',
                           json={'email': 'test1@unsw.au', 'password': 'password1', 'name_first': 'test1', 'name_last': 'last1'})
    member_1_details = member.json()
    return member_1_details


@pytest.fixture
def channel(admin):
    return requests.post(config.url + '/channels/create/v2', json={'token': admin['token'], 'name': 'channel_1', 'is_public': True}).json()


@ pytest.fixture
def dm(admin, member):
    return requests.post(config.url + '/dm/create/v1', json={'token': admin['token'], 'u_ids': [member['auth_user_id']]}).json()


@ pytest.fixture
def channel_messages(admin, channel):
    requests.post(config.url + '/message/send/v2', json={
                  'token': admin['token'], 'channel_id': channel['channel_id'], 'message': 'this is a message sent to the other user in the channel.'}).json()
    requests.post(config.url + '/message/send/v2', json={'token': admin['token'], 'channel_id': channel['channel_id'],
                                                         'message': 'this is a message sent to the other user in the channel11111.'}).json()
    requests.post(config.url + '/message/send/v2', json={'token': admin['token'], 'channel_id': channel['channel_id'],
                                                         'message': 'this is a message sent to the other user in the channel2222222.'}).json()


@ pytest.fixture
def dm_messages(admin, dm):
    requests.post(config.url + '/message/senddm/v1', json={
                  'token': admin['token'], 'dm_id': dm['dm_id'], 'message': 'this is a message sent to the other user.'}).json()
    requests.post(config.url + '/message/senddm/v1', json={
                  'token': admin['token'], 'dm_id': dm['dm_id'], 'message': 'this is a message sent to the other user.111111'}).json()
    requests.post(config.url + '/message/senddm/v1', json={
                  'token': admin['token'], 'dm_id': dm['dm_id'], 'message': 'this is a message sent to the other user2222222222.'}).json()


def test_invalid_token_dm(dm_messages):
    invalid_token = 'invalidtoken123123'
    search_response = requests.get(config.url + '/search/v2', params={
        'token': invalid_token, 'query_str': 'this is an updated message in the dm.'})
    assert search_response.status_code == 403


def test_query_string_length_incorrect(admin, channel_messages):
    search_response = requests.get(config.url + '/search/v2', params={
        'token': admin['token'], 'query_str': 1500 * 'A'})
    assert search_response.status_code == 400


def test_success_case(admin, channel_messages, dm_messages):
    search_result = requests.get(config.url + '/search/v2', params={
        'token': admin['token'], 'query_str': '111'}).json()

    list_of_messages = []
    for message in search_result['messages']:
        list_of_messages.append(message['message'])

    assert 'this is a message sent to the other user in the channel11111.' in list_of_messages
    assert 'this is a message sent to the other user.111111' in list_of_messages
    assert len(list_of_messages) == 2
