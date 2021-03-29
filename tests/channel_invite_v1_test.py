import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_join_v1, channel_invite_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

#Need to make a decision about global owners and whether they have access

@pytest.fixture
def user1():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v1(email,password,firstname, lastname)

@pytest.fixture
def user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email,password,firstname, lastname)

@pytest.fixture
def channel_id():
    name = "Testchannel"
    user_id = auth_register_v1("channelcreator@gmail.com", "TestTest", "channelcreator", "last")['auth_user_id']
    return channels_create_v1(user_id, name, True)['channel_id']

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_channel_id(clear, user1, user2):
    with pytest.raises(InputError):
        channel_invite_v1(user1['token'], 1, user2['auth_user_id'])
    clear_v1() 

def test_invalid_u_id(clear, channel_id):
    auth_user = auth_login_v1("channelcreator@gmail.com", "TestTest")
    user_id = auth_user['auth_user_id'] + 1
    with pytest.raises(InputError):
        channel_invite_v1(auth_user['token'], channel_id, user_id)
    clear_v1() 

def test_unauthorised_user(clear, user1, user2, channel_id):
    with pytest.raises(AccessError):
        channel_invite_v1(user2['token'], channel_id, user1['auth_user_id'])
    clear_v1() 

def test_all_valid(clear, user1, channel_id):
    auth_user = auth_login_v1("channelcreator@gmail.com", "TestTest")
    assert channel_invite_v1(auth_user['token'], channel_id, user1['auth_user_id']) == {}
    clear_v1() 

def test_user_already_in_channel(clear, user1, channel_id):
    auth_user = auth_login_v1("channelcreator@gmail.com", "TestTest")
    channel_invite_v1(auth_user_id['token'], channel_id, user1['auth_user_id'])
    assert channel_invite_v1(auth_user_id['token'], channel_id, user1['auth_user_id']) == {}
    clear_v1()

def test_invalid_token(clear, user1, channel_id):
    with pytest.raises(AccessError):
        channel_invite_v1('bad.token.given', channel_id, user1['auth_user_id'])
    clear_v1()