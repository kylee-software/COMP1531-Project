import users, channels from data.py
import pytest

@pytest.fixture
def call_clear():
    # call the clear function from the project to reset all data
    clear_v1()

@pytet.fixture
def create_user():
    # create a test user and return the id
    return auth_register_v1("testemail@gmail.com", "TestPassword1", "firstname", "lastname")

@pytest.fixture
def create_channel(user_id, is_public):
    # create a test channel and return the id
    return channel_create_v1(user_id, "TestChannel", is_public)


def test_channel_id():
    # want to check channel_id that does not exist - InputError
    assert
    # want to check channel_id that does exist
    assert 


def test_user_existance():
# User not exist error: user id doesnt exist --> should be Input I think
# check using an existing id
# check using a not existing id

def test_user_access():

# AccessError: auth_id is not part of channel
# want to check auth_id is in channel
# check auth_id that is not in channel
