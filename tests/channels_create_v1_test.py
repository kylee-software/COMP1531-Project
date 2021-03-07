import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError


@pytest.fixture
def create_user():
    # reset all data
    clear_v1()
    # create a test user and return auth_id
    email = "testmail@gamil.com"
    password = "Testpass12345"
    auth_user_id = auth_register_v1(email, password, "firstname", "lastname")
    return auth_user_id


def test_invalid_name():
    # Test invalid name with more tan 20 characters --> "InputError"
    auth_user_id = create_user()
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id, "fffffffffffffffffffff", True)


def test_valid_name_public():
    # Given a valid name and is_public set to true, assert that the return value channel_id is a dictionary
    auth_user_id = create_user()
    assert channels_create_v1(auth_user_id, "channelName1", True) == {'channel_id': 1}


def test_valid_name_private():
    # Given a valid name and is_public set to false, assert that the return value channel_id is a dictionary
    auth_user_id = create_user()
    assert channels_create_v1(auth_user_id, "channelName2", False) == {'channel_id': 2}


def test_invalid_authId():
    clear_v1()
    auth_user_id = 4
    with pytest.raises(AccessError):
        channels_create_v1(auth_user_id, "channelName3", True)


