import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError


@pytest.fixture
def create_user():
    # reset all data
    clear_v1()
    # create a test user and return auth id
    return auth_register_v1("testmail@gamil.com", "Testpass12345", "firstname", "lastname")['user_id']
    # return type = {'user_id : int}

def test_invalid_name():
    # Test invalid name with more tan 20 characters --> "InputError"
    with pytest.raises(InputError):
        channels_create_v1(create_user, "fffffffffffffffffffff", True)


def test_valid_name_public():
    # Given a valid name and is_public set to true, assert that the return value channel_id is a dictionary
    assert type(channels_create_v1(create_user, "channelName1", True)) is dict


def test_valid_name_private():
    # Given a valid name and is_public set to false, assert that the return value channel_id is a dictionary
    assert type(channels_create_v1(create_user, "channelName2", False)) is dict


