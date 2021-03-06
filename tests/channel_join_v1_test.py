import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

@pytest.fixture
def create_user():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email,password,firstname, lastname)['auth_user_id']

@pytest.fixture
def create_public_channel():
    name = "Testchannel"
    user_id = auth_register_v1("channelcreator@gmail.com", "TestTest1", "channelcreator", "lastname")
    return channels_create_v1(user_id, name, True)['channel_id']

@pytest.fixture
def create_private_channel():
    name = "Testchannel"
    user_id = auth_register_v1("channelcreator@gmail.com", "TestTest1", "channelcreator", "lastname")
    return channels_create_v1(user_id, name, False)['channel_id']

clear_v1()
def test_valid_channel_id_public(create_public_channel, create_user):

    assert channel_join_v1(create_user, create_public_channel) == {}

clear_v1()
def test_invalid_channel_id(create_user):
    
    with pytest.raises(InputError):
        channel_join_v1(create_user, 1) 

clear_v1()
def test_global_user_private_channel(create_user, create_pivate_channel):

    assert channel_join_v1(create_user, create_private_channel) == {}

clear_v1()
def test_not_global_user_private_channel(create_private_channel, create_user):

    with pytest.raises(AccessError):
        channel_join_v1(create_user, create_private_channel) == {}

clear_v1()
def test_channel_member_joining_again(create_user):
    
    channel_id = channel_create_v1(create_user, "testchannel", True)['channel_id']
    assert channel_join_v1(create_user, channel_id) == {}



