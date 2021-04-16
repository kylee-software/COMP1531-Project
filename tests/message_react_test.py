import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channel import channel_join_v1
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.message import message_react_v1, message_senddm_v1, message_send_v2
from src.error import InputError, AccessError

@pytest.fixture
def owner():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    owner = auth_register_v2(email, password, "firstname", "lastname")['token']
    return owner

@pytest.fixture
def member():
    member_info = auth_register_v2("testmail1@gmail.com", "Testpass123456", "memberfirst", "memberlast")
    return member_info

@pytest.fixture
def channel_message_id(owner, member):
    channel_id = channels_create_v2(owner, "channelName", True)['channel_id']
    channel_join_v1(member['token'], channel_id)
    message_id = message_send_v2(owner, channel_id, "Hi!")['message_id']
    return message_id

@pytest.fixture
def dm_message_id(owner, member):
    dm_id = dm_create_v1(owner, [member['auth_user_id']])['dm_id']
    message_id = message_senddm_v1(member['token'], dm_id, "Hi!")['message_id']
    return message_id

@pytest.fixture
def clear():
    return clear_v1()

def test_invalid_token(clear, dm_message_id):
    with pytest.raises(AccessError):
        message_react_v1("invalid_owner", dm_message_id, 1)

def test_user_not_a_member(clear, channel_message_id, dm_message_id):
    non_member = auth_register_v2("testmail2@gmail.com", "Testpass123456", "nota", "member")['token']
    with pytest.raises(AccessError):
        message_react_v1(non_member, channel_message_id, 1)
        message_react_v1(non_member, dm_message_id, 1)

def test_invalid_message_id(clear, owner, channel_message_id, dm_message_id):
    with pytest.raises(InputError):
        message_react_v1(owner, channel_message_id + 1, 1)
        message_react_v1(owner, dm_message_id + 1, 1)

def test_invalid_react_id(clear, owner, channel_message_id, dm_message_id):
    with pytest.raises(InputError):
        message_react_v1(owner, channel_message_id, 0)
        message_react_v1(owner, dm_message_id, 0)

def test_react_twice(clear, owner, member, channel_message_id, dm_message_id):
    message_react_v1(member['token'], channel_message_id, 1)
    message_react_v1(owner, dm_message_id, 1)

    with pytest.raises(InputError):
        message_react_v1(member['token'], channel_message_id, 1)
        message_react_v1(owner, dm_message_id, 1)

def test_message_react(clear, owner, member, channel_message_id, dm_message_id):
    assert message_react_v1(member['token'], channel_message_id, 1) == {}
    assert message_react_v1(owner, dm_message_id, 1) == {}