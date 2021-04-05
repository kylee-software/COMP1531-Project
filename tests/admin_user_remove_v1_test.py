import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1, dm_details_v1
from src.admin import admin_changepermission_v1,admin_user_remove_v1
from src.channels import channels_create_v2
from src.channel import channel_join_v1, channel_messages_v2, channel_removeowner_v1
from src.message import message_senddm_v1, message_send_v2, message_remove_v1
from src.error import InputError, AccessError


@pytest.fixture
def clear():
    clear_v1()

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

def test_invalid_token(clear, member):
    with pytest.raises(AccessError):
        admin_user_remove_v1("invalid_token", member['auth_user_id'])

def test_not_dream_owner(clear, global_owner, member):
    with pytest.raises(AccessError):
        admin_user_remove_v1(member['token'], member['auth_user_id'])

def test_invalid_u_id(clear, global_owner):
    with pytest.raises(InputError):
        admin_user_remove_v1(global_owner['token'], 6)

def test_only_owner(clear, global_owner, owner2):
    admin_user_remove_v1(global_owner['token'], owner2['auth_user_id'])
    with pytest.raises(InputError):
        admin_user_remove_v1(global_owner['token'], global_owner['auth_user_id'])

def test_user_in_channel(clear, global_owner, owner2, member, channel_id):
    admin_user_remove_v1(global_owner['token'], member['auth_user_id'])
    messages = channel_messages_v2(global_owner['token'], channel_id, 0)['messages']
    assert messages[0]['message'] == "Removed user"

def test_user_in_dm(clear, global_owner, owner2, member, dm_id):
    admin_user_remove_v1(global_owner['token'], member['auth_user_id'])
    messages = dm_messages_v1(global_owner['token'], dm_id, 0)['messages']
    assert messages[0]['message'] == "Removed user"

def test_owner_is_only_channel_owner(clear, global_owner, owner2, channel_id):
    with pytest.raises(InputError):
        admin_user_remove_v1(owner2['token'], global_owner['auth_user_id'])

def test_owner_is_creator(clear, global_owner, owner2, channel_id, dm_id):
    admin_user_remove_v1(owner2['token'], global_owner['auth_user_id'])
    with pytest.raises(InputError):
        dm_details_v1(owner2['token'], dm_id)  # raises InputError when dm does not exists