import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.channels import channels_create_v2
from src.channel import channel_join_v1, channel_messages_v2
from src.message import message_senddm_v1, message_send_v2, message_remove_v1
from src.error import InputError, AccessError
from src.helper import load_data


@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def auth_user():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    auth_user_info = auth_register_v2(email, password, "firstname", "lastname")
    token = auth_user_info['token']
    return token

@pytest.fixture
def member():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firstone"
    last_name = "lastone"
    member = auth_register_v2(email, password, first_name, last_name)
    return member

@pytest.fixture
def channel_id(auth_user, member):
    channel_id = channels_create_v2(auth_user, "channelName", True)['channel_id']
    channel_join_v1(member['token'], channel_id)
    return channel_id

@pytest.fixture
def dm_id(auth_user, member):
    dm_id = dm_create_v1(auth_user, [member['auth_user_id']])['dm_id']
    return dm_id

def test_remove_channel_message(clear, auth_user, channel_id):
    message_id = message_send_v2(auth_user, channel_id, "Hi!")
    channel_messages_count_before = len(channel_messages_v2(auth_user, channel_id, 0)['messages'])
    assert channel_messages_count_before == 1

    message_remove_v1(auth_user, message_id)
    with pytest.raises(InputError):
        channel_messages_v2(auth_user, channel_id, 0)

def test_remove_dm_message(clear, auth_user, dm_id):
    message_id = message_senddm_v1(auth_user, dm_id, "Hi!")['message_id']
    dm_messages_count_before = len(dm_messages_v1(auth_user, dm_id, 0)['messages'])
    assert dm_messages_count_before == 1

    message_remove_v1(auth_user, message_id)
    with pytest.raises(InputError):
        dm_messages_v1(auth_user, dm_id, 0)

def test_invalid_token(clear, auth_user, channel_id):
    channel_message_id = message_send_v2(auth_user, channel_id, "Hi!")
    with pytest.raises(AccessError):
        message_remove_v1("invalid_token", channel_message_id)

def test_unauthorised_auth_user(clear, auth_user, member, channel_id, dm_id):
    # Test when a auth_user is not the sender nor an owner of the channel owner nor an owner of Dreams
    channel_message_id = message_send_v2(auth_user, channel_id, "Hi!")
    dm_message_id = message_senddm_v1(auth_user, dm_id, "Hi!")['message_id']

    with pytest.raises(AccessError):
        message_remove_v1(member['token'], channel_message_id)
        message_remove_v1(member['token'], dm_message_id)

def test_invalid_message_id(clear, auth_user):
    with pytest.raises(InputError):
        message_remove_v1(auth_user, 1)

