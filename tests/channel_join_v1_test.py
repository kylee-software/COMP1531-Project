import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError


@pytest.fixture
def user1():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email, password, firstname, lastname)['auth_user_id']


@pytest.fixture
def public_channel_id():
    name = "Testchannel"
    user_id = auth_register_v2(
        "channelcreator@gmail.com", "TestTest1", "channelcreator", "lastname")['auth_user_id']
    return channels_create_v1(user_id, name, True)['channel_id']


@pytest.fixture
def private_channel_id():
    name = "Testchannel"
    user_id = auth_register_v2("channelcreator1@gmail.com",
                               "TestTest1", "channelcreator1", "lastname1")['auth_user_id']
    return channels_create_v1(user_id, name, False)['channel_id']


@pytest.fixture
def clear():
    clear_v1()


def test_valid_channel_id_public(clear, create_public_channel, create_user):

    assert channel_join_v1(create_user, create_public_channel) == {}
    clear_v1()


def test_invalid_channel_id(clear, create_user):

    with pytest.raises(InputError):
        channel_join_v1(create_user, 1)
    clear_v1()


def test_global_user_private_channel(clear, user1, private_channel_id):

    assert channel_join_v1(create_user, create_private_channel) == {}
    clear_v1()


def test_not_global_user_private_channel(clear, private_channel_id, create_user):

    with pytest.raises(AccessError):
        channel_join_v1(create_user, create_private_channel) == {}
    clear_v1()


def test_channel_member_joining_again(clear, create_user):

    channel_id = channels_create_v1(
        create_user, "testchannel", True)['channel_id']
    assert channel_join_v1(create_user, channel_id) == {}
    clear_v1()
