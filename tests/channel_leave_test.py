import pytest
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channel import channel_invite_v1, channel_leave_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

@pytest.fixture
def user1():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def channel_id():
    name = "Testchannel"
    owner_id = auth_register_v2("channelcreator@gmail.com", "TestTest1", "first", "last")["auth_user_id"]
    return channels_create_v1(owner_id, name, True)['channel_id']

@pytest.fixture
def channel_owner():
    return auth_login_v2("channelcreator@gmail.com", "TestTest1")

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_channel_id(clear, channel_id, channel_owner,):
    with pytest.raises(InputError):
        channel_leave_v1(channel_owner['token'], channel_id + 1)
    clear_v1()

def test_invalid_token(clear, channel_id):
    with pytest.raises(AccessError):
        channel_leave_v1('invalid.token.input', channel_id)
    clear_v1()

def test_invalid_auth_user_id(clear, channel_id, channel_owner):
    #can this happen if the token is being checked
    pass

def test_user_not_member(clear, channel_id, user1):
    with pytest.raises(AccessError):
        channel_leave_v1(user1['token'], channel_id)
    clear_v1()

def test_owner_user(clear, channel_id, channel_owner):
    assert channel_leave_v1(channel_owner['token'], channel_id) == {}
    
    with pytest.raises(AccessError):
        channel_details_v1(channel_owner['token'], channel_id)
    clear_v1() 

def test_not_owner_user(clear, channel_id, channel_owner, user1):
    channel_invite_v1(channel_owner['token'], channel_id, user1['auth_user_id'])
    assert channel_leave_v1(user1['token'], channel_id) == {}
    
    with pytest.raises(AccessError):
        channel_details_v1(user1['token'], channel_id)
    clear_v1() 

