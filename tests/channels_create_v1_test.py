import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1


@pytest.fixture
def call_clear():
    # rest the all data
    clear_v1()


@pytest.fixture
def create_user():
    # create a test user and return auth id
    return auth_register_v1("testmail@gamil.com", "Testpass12345", "firstname", "lastname")


def test_invalid_name():
    # Test invalid name with more tan 20 characters --> "InputError"
    assert channels_create_v1(create_user, "fffffffffffffffffffff", "is_public") == "Name is more than 20 characters " \
                                                                                    "long! "


def test_valid_name_public():
    # Given a valid name and is_public set to true, assert that the return value channel_id is an integer
    assert type(channels_create_v1(create_user, "channelName1", True)) is int


def test_valid_name_private():
    # Given a valid name and is_public set to false, assert that the return value channel_id is an integer
    assert type(channels_create_v1(create_user, "channelName2", False)) is int


