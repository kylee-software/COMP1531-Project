import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channel import channel_join_v1, channel_removeowner_v1
from src.channels import channels_create_v2
from src.error import InputError, AccessError


@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def owner():
    email = "testmail1@gamil.com"
    password = "Testpass12345"
    user_info = auth_register_v2(email, password, "firstone", "lastone")
    return user_info

@pytest.fixture
def member():
    email = "testmail2@gamil.com"
    password = "Testpass123456"
    user_info = auth_register_v2(email, password, "firsttwo", "lasttwo")
    return user_info

@pytest.fixture
def channel_id(owner, member):
    channel_id = channels_create_v2(owner['token'], "channelName1", True)['channel_id']
    channel_join_v1(member['token'], channel_id) # owner is now an owner of this new channel
    return channel_id


def test_invalid_token(clear, channel_id, member):
    with pytest.raises(AccessError):
        channel_removeowner_v1("Invalid token", channel_id, member['auth_user_id'])

def test_invalid_channel_id(clear, owner, channel_id, member):
    with pytest.raises(InputError):
        channel_removeowner_v1(owner['token'], channel_id + 1, member['auth_user_id'])

def test_user_not_owner(clear, owner, channel_id):
    with pytest.raises(InputError):
        channel_removeowner_v1(owner['token'], channel_id, 5)

def test_remove_only_owner(clear, owner, channel_id):
    with pytest.raises(InputError):
        channel_removeowner_v1(owner['token'], channel_id, owner['auth_user_id'])

def test_token_not_owner(clear, channel_id, owner):
    not_owner = auth_register_v2("testemail@gmail.com", "password111", "firstthree", "lastthree")['token']
    with pytest.raises(AccessError):
        channel_removeowner_v1(not_owner, channel_id, owner['auth_user_id'])


