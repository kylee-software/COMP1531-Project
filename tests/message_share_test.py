import pytest
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channel import channel_join_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.message import message_share_v1, message_senddm_v1, message_send_v1

@pytest.fixture
def user1():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user3():
    email = "test3email@gmail.com"
    password = "TestTest3"
    firstname = "firstname3"
    lastname = "lastname3"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def channel_id():
    name = "Testchannel"
    owner_id = auth_register_v2("channelcreator@gmail.com", "TestTest1", "first", "last")["auth_user_id"]
    return channels_create_v1(owner_id, name, True)['channel_id']

@pytest.fixture
def dm(user2, user3):
    return dm_create_v1(user2['token'], [user3['auth_user_id']])


@pytest.fixture
def clear():
    clear_v1()


def test_invalid_token(clear, channel_id, user1, dm):


def test_invalid_og_message_id():

def test_message_too_long():

def test_invalid_channel_id():

def test_invalid_dm_id():

def test_dm_not_1():

def test_channel_not_1():

def test_user_not_in_channel():

def test_user_not_in_dm():

def test_share_to_channel():

def test_share_to_dm():