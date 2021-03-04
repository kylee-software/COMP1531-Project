import pytest

from src.channels import channels_create_v1, channels_list_v1
from src.auth import auth_register_v1
from src.error import AccessError
from src.other import clear_v1

@pytest.fixture
def auth_user_id():
    return auth_register_v1("test@test.unsw.com", 'testPassword8', 'Test', "User")

"""@pytest.fixture
def names():
    return ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']"""


def test_lists_a_single_channel(auth_user_id):
    clear_v1()
    channels_create_v1(auth_user_id, 'testChannel01', False)
    assert len(channels_list_v1(auth_user_id)) == 1

def test_correct_single_channel_listed(auth_user_id):
    clear_v1()
    channels_create_v1(auth_user_id, 'testChannel01', False)
    returnList = channels_list_v1(auth_user_id)
    foundChannel = False
    for channels in returnList:
        for key, value in channels.item():
            if value == 'testChannel01': foundChannel = True

    assert foundChannel == True


def test_multiple_channels(auth_user_id):
    clear_v1()
    channels_create_v1(auth_register_v1, 'testChannel01', False)
    channels_create_v1(auth_register_v1, 'testChannel02', False)
    assert len(channels_list_v1(auth_user_id)) == 2

def test_correct_multiple_channels_listed(auth_user_id):
    clear_v1()
    channels_create_v1(auth_user_id, 'testChannel01', False)
    channels_create_v1(auth_user_id, 'testChannel02', False)
    returnList = channels_list_v1(auth_user_id)
    foundChannel = False
    foundChannel2 = False
    for channels in returnList:
        for key, value in channels.item():
            if value == 'testChannel01': foundChannel = True
            elif value == 'testChannel02': foundChannel2 = True
    assert foundChannel == True and foundChannel2 == True

def test_cant_see_other_user_channels(auth_user_id):
    auth_user_id02 = auth_register_v1("test02@test.unsw.com", 'testPassword8', 'Test02', "User")
    channels_create_v1(auth_user_id, 'testChannel01', False)
    channels_create_v1(auth_user_id02, 'testChannel02', False)
    returnList = channels_list_v1(auth_user_id)
    foundChannel = False
    foundWrongChannel = False
    for channels in returnList:
        for key, value in channels.item():
            if value == 'testChannel01': foundChannel = True
            elif value == 'testChannel02': foundWrongChannel = True
    assert foundChannel == True and foundWrongChannel == False

def test_invalid_authid():
    clear_v1()
    auth_user_id = 4
    with pytest.raises(AccessError):
        channels_list_v1(auth_user_id)

