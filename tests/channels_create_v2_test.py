import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError


@pytest.fixture
def token():
    # reset all data
    clear_v1()
    # create a test user and return auth_id
    email = "testmail@gamil.com"
    password = "Testpass12345"
    token = auth_register_v2(email, password, "firstname", "lastname")['token']
    return token


def test_invalid_name(token):
    # Test invalid name with more tan 20 characters or no name is entered --> "InputError"
    with pytest.raises(InputError):
        channels_create_v2(token, "", True)
        channels_create_v2(token, "fffffffffffffffffffff", True)


def test_valid_name_public(token):
    # Given a valid name and is_public set to true, assert that the return value channel_id is a dictionary
    assert channels_create_v2(token, "channelName1", True) == {'channel_id': 1}


def test_valid_name_private(token):
    # Given a valid name and is_public set to false, assert that the return value channel_id is a dictionary
    assert channels_create_v2(token, "channelName2", False) == {'channel_id': 1}


def test_invalid_token():
    with pytest.raises(AccessError):
        channels_create_v2("invalid_token", "channelName3", True)


def test_valid_channel_id(token):
    channel_id = channels_create_v2(token, 'channel_name', True)['channel_id']
    assert channel_id == 1

