import pytest
import requests
from src import config
from src.helper import is_valid_token, create_token


@pytest.fixture
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


def test_invalid_token(clear, create_admin, create_member_1):

    admin_invalid_token = 'invalidtoken123123'
    admin = create_admin
    member = create_member_1
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin_invalid_token, 'channel_id': channel_id['channel_id'], 'u_id': member['auth_user_id']})
    assert addowner.status_code == 403


def test_invalid_channel(clear, create_admin, create_member_1):
    admin = create_admin
    member = create_member_1
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin['token'], 'channel_id': 1, 'u_id': member['auth_user_id']})
    assert addowner.status_code == 400


def test_user_nonexistent(clear, create_admin):
    admin = create_admin
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin['token'], 'channel_id': channel_id['channel_id'], 'u_id': 10})
    assert addowner.status_code == 400


def test_user_already_owner(clear, create_admin, create_member_1):
    admin = create_admin
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin['token'], 'channel_id': channel_id['channel_id'], 'u_id': admin['auth_user_id']})
    assert addowner.status_code == 400


def test_not_owner_of_channel_or_dreams(clear, create_admin, create_member_1):
    admin = create_admin
    member_1 = create_member_1
    member_2 = requests.post(config.url + '/auth/register/v2',
                             json={'email': 'test2@unsw.au', 'password': 'password2', 'name_first': 'test2', 'name_last': 'last2'})
    member_2_details = member_2.json()
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': member_1['token'], 'channel_id': channel_id['channel_id'], 'u_id': member_2_details['auth_user_id']})
    assert addowner.status_code == 403


def test_successful_addowner(clear, create_admin, create_member_1):
    admin = create_admin
    member = create_member_1
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_details = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin['token'], 'channel_id': channel_details['channel_id'], 'u_id': member['auth_user_id']})
    assert addowner.status_code == 200
