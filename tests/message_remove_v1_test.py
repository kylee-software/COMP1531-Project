import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.admin import admin_changepermission_v1
from src.channels import channels_create_v2
from src.channel import channel_join_v1, channel_messages_v2
from src.message import message_senddm_v1, message_send_v2, message_remove_v1
from src.error import InputError, AccessError

@pytest.fixture
def member():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firstone"
    last_name = "lastone"
    member = auth_register_v2(email, password, first_name, last_name)
    return member

@pytest.fixture
def auth_user():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    auth_user_info = auth_register_v2(email, password, "firstname", "lastname")
    token = auth_user_info['token']
    u_id = auth_user_info['auth_user_id']
    admin_changepermission_v1(token, u_id, 1) # Make the auth_user an owner of Dreams
    return token

@pytest.fixture
def channel_message_info(auth_user, member):
    channel_id = channels_create_v2(auth_user, "channelName", True)['channel_id']
    channel_join_v1(member['token'], channel_id)
    message_id = message_send_v2(auth_user, channel_id, "Hi!")
    return [channel_id, message_id]

@pytest.fixture
def dm_message_info(auth_user, member):
    dm_id = dm_create_v1(auth_user, [member['auth_user_id']])['dm_id']
    message_id = message_senddm_v1(auth_user, dm_id, "Hi!")
    return [dm_id, message_id]

def test_remove_messages(auth_user, channel_message_info, dm_message_info):
    clear_v1()
    channel_id = channel_message_info[0]
    channel_message_id = channel_message_info[1]
    dm_id = dm_message_info[0]
    dm_message_id = dm_message_info[1]

    channel_messages_count_before = len(channel_messages_v2(auth_user, channel_id, 0)['messages'])
    dm_messages_count_before = len(dm_messages_v1(auth_user, dm_id, 0)['messages'])

    # Make sure that the messages are added
    assert channel_messages_count_before == 1
    assert dm_messages_count_before == 1

    # Remove messages
    message_remove_v1(auth_user, channel_message_id)
    message_remove_v1(auth_user, dm_message_id)

    channel_messages_count_after = len(channel_messages_v2(auth_user, channel_id, 0)['messages'])
    dm_messages_count_after = len(dm_messages_v1(auth_user, dm_id, 0)['messages'])

    # Ensured that the messages are removed i.e. the message_remove function works
    assert channel_messages_count_after == 0
    assert dm_messages_count_after == 0

def test_invalid_token(dm_message_info):
    clear_v1()
    with pytest.raises(AccessError):
        message_remove_v1("invalid_token", dm_message_info[1])

def test_unauthorised_auth_user(member, channel_message_info, dm_message_info):
    clear_v1()
    # Test when a auth_user is not the sender nor an owner of the channel owner nor an owner of Dreams
    with pytest.raises(AccessError):
        message_remove_v1(member['token'], channel_message_info[1])
        message_remove_v1(member['token'], dm_message_info[1])

def test_invalid_message_id(auth_user, channel_message_info, dm_message_info):
    clear_v1()
    with pytest.raises(InputError):
        message_remove_v1(auth_user, channel_message_info[1])
        message_remove_v1(auth_user, dm_message_info[1])
