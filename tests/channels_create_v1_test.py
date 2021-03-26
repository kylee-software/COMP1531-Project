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
    return auth_user_id['auth_user_id']


def test_invalid_name(create_user):
    # Test invalid name with more tan 20 characters --> "InputError"
    with pytest.raises(InputError):
        channels_create_v1(create_user, "fffffffffffffffffffff", True)
    clear_v1() 


def test_valid_name_public(create_user):
    # Given a valid name and is_public set to true, assert that the return value channel_id is a dictionary
    assert channels_create_v1(create_user, "channelName1", True) == {'channel_id': 1}
    clear_v1() 


def test_valid_name_private(create_user):
    # Given a valid name and is_public set to false, assert that the return value channel_id is a dictionary
    assert channels_create_v1(create_user, "channelName2", False) == {'channel_id': 1}
    clear_v1() 


def test_invalid_authId():
    clear_v1()
    auth_user_id = 4
    with pytest.raises(AccessError):
        channels_create_v1(auth_user_id, "channelName3", True)
    clear_v1() 


