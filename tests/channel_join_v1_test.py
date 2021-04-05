import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channel import channel_join_v1
from src.channels import channels_create_v2
from src.error import InputError, AccessError


@pytest.fixture
def user1():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email, password, firstname, lastname)


@pytest.fixture
def public_channel_id():
    name = "Testchannel"
    user = auth_register_v2(
        "channelcreator@gmail.com", "TestTest1", "channelcreator", "lastname")
    return channels_create_v2(user['token'], name, True)['channel_id']


@pytest.fixture
def private_channel_id():
    name = "Testchannel"
    user = auth_register_v2("channelcreator1@gmail.com",
                               "TestTest1", "channelcreator1", "lastname1")
    return channels_create_v2(user['token'], name, False)['channel_id']


@pytest.fixture
def clear():
    clear_v1()

def test_valid_channel_id_public(clear, public_channel_id, user1):

    assert channel_join_v1(user1['token'], public_channel_id) == {}
    clear_v1() 


def test_invalid_channel_id(clear, user1):
    
    with pytest.raises(InputError):
        channel_join_v1(user1['token'], 1) 
    clear_v1() 


def test_global_user_private_channel(clear, user1, private_channel_id):

    assert channel_join_v1(user1['token'], private_channel_id) == {}
    clear_v1() 


def test_not_global_user_private_channel(clear, private_channel_id, user1):

    with pytest.raises(AccessError):
        channel_join_v1(user1['token'], private_channel_id) == {}
    clear_v1() 


def test_channel_member_joining_again(clear, user1):
    
    channel_id = channels_create_v2(user1['token'], "testchannel", True)['channel_id']
    assert channel_join_v1(user1['token'], channel_id) == {}
    clear_v1() 

def test_invalid_token(clear, public_channel_id, user1):
    with pytest.raises(AccessError):
        channel_join_v1('bad.token.given', public_channel_id)

