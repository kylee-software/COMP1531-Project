import pytest
import requests
import json
from src import config
import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.admin import admin_changepermission_v1
from src.channels import channels_create_v2
from src.channel import channel_join_v1, channel_messages_v2, channel_addowner_v1
from src.message import message_senddm_v1, message_send_v2, message_remove_v1
from src.error import InputError, AccessError


@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

@pytest.fixture
def user():
    email = "testmail@gamil.com"
    password = "Testpass123"
    first_name = "first"
    last_name = "last"

    token = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['token']

    return token


def test_invalid_input(clear, user):
    resp = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': user,
        'u_id': "ab",
    })

    status_code = resp.status_code
    assert status_code == 400


@pytest.fixture
def global_owner():
    email = "testmail1@gmail.com"
    password = "Testpass1"
    first_name = "firstone"
    last_name = "lastone"
    user_info = auth_register_v2(email, password, first_name, last_name)
    return user_info

@pytest.fixture
def owner2(global_owner):
    email = "testmail2@gmail.com"
    password = "Testpass2"
    first_name = "firsttwo"
    last_name = "lasttwo"
    user_info = auth_register_v2(email, password, first_name, last_name)
    admin_changepermission_v1(global_owner['token'], user_info['auth_user_id'], 1) # Make the user an owner of Dreams
    return user_info

@pytest.fixture
def member():
    email = "testmail3@gmail.com"
    password = "Testpass3"
    first_name = "firstthree"
    last_name = "lastthree"
    user_info = auth_register_v2(email, password, first_name, last_name)
    return user_info

@pytest.fixture
def channel_id(global_owner, member):
    channel_id = channels_create_v2(global_owner['token'], "channelName", True)['channel_id']
    channel_join_v1(member['token'], channel_id)
    message_send_v2(member['token'], channel_id, "Hi!")
    return channel_id

@pytest.fixture
def dm_id(global_owner, member):
    dm_id = dm_create_v1(global_owner['token'], [member['auth_user_id']])['dm_id']
    message_senddm_v1(member['token'], dm_id, "Hi!")
    return dm_id


def test_user_in_channel(clear, global_owner, owner2, member, channel_id):
    requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': global_owner['token'],
        'u_id': member['auth_user_id'],
    })

    messages = channel_messages_v2(global_owner['token'], channel_id, 0)['messages']
    assert messages[0]['message'] == "Removed user"
