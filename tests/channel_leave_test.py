import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_join_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

@pytest.fixture
def user1():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email,password,firstname, lastname)

@pytest.fixture
def channel_id():
    name = "Testchannel"
    owner_id = auth_register_v1("channelcreator@gmail.com", "TestTest1", "first", "last")["auth_user_id"]
    return channels_create_v1(owner_id, name, True)['channel_id']

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_channel_id(clear, user):

def test_invalid_token():

def test_invalid_auth_user_id():

def test_user_not_member():

def test_owner_user():

def test_not_owner_user():

