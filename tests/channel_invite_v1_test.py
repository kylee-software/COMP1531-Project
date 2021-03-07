import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_join_v1, channel_invite_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

#Need to make a decision about global owners and whether they have access

@pytest.fixture
def create_user1():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v1(email,password,firstname, lastname)['auth_user_id']

@pytest.fixture
def create_user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email,password,firstname, lastname)['auth_user_id']

@pytest.fixture
def create_public_channel():
    name = "Testchannel"
    user_id = auth_register_v1("channelcreator@gmail.com", "TestTest", "channelcreator", "last")
    return channels_create_v1(user_id, name, True)['channel_id']

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_channel_id(clear, create_user1, create_user2):
    with pytest.raises(InputError):
        channel_invite_v1(create_user1, 1, create_user2)

def test_invalid_u_id(clear, create_public_channel):
    auth_user_id = auth_login_v1("channelcreator@gmail.com", "TestTest")['auth_user_id']
    user_id = auth_user_id + 1
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id, create_public_channel, user_id)

def test_unauthorised_user(clear, create_user1, create_user2, create_public_channel):
    with pytest.raises(AccessError):
        channel_invite_v1(create_user2, create_public_channel, create_user1)

def test_all_valid(clear, create_user1, create_public_channel):
    auth_user_id = auth_login_v1("channelcreator@gmail.com", "TestTest")['auth_user_id']
    assert channel_invite_v1(auth_user_id, create_public_channel, create_user1) == {}

def test_user_already_in_channel(clear, create_user1, create_public_channel):
    auth_user_id = auth_login_v1("channelcreator@gmail.com", "TestTest")['auth_user_id']
    channel_invite_v1(auth_user_id, create_public_channel, create_user1)
    assert channel_invite_v1(auth_user_id, create_public_channel, create_user1) == {}
    