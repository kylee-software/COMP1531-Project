import pytest

from src.channels import channels_create_v1, channels_list_v1
from src.auth import auth_register_v1
from src.error import AccessError
from src.other import clear_v1

@pytest.fixture
def auth_user_id():
    return auth_register_v1("test@test.unsw.com", 'testPassword8', 'Test', "User")

@pytest.fixture
def names():
    return ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']

def test_no_channels(auth_user_id):
    clear_v1()
    returnDict = channels_list_v1(auth_user_id)
    assert returnDict['channels'] == []

def test_lists_a_single_channel(auth_user_id):
    clear_v1()
    channels_create_v1(auth_user_id, 'testChannel01', False)
    returnDict = channels_list_v1(auth_user_id)
    assert len(returnDict['channels']) == 1

def test_can_see_five_channels(auth_user_id, names):
    clear_v1()
    for name in names:
        channels_create_v1(auth_register_v1, name, False)
    returnDict = channels_list_v1(auth_user_id)
    assert len(returnDict['channels']) == 5

def test_can_only_see_one_of_six(auth_user_id, names):
    auth_user_id02 = auth_register_v1("test02@test.unsw.com", 'testPassword16', 'Test02', "User")
    for name in names:
        channels_create_v1(auth_register_v1, name, False)
    channels_create_v1(auth_user_id02, 'testChannel06', False)
    returnDict = channels_list_v1(auth_user_id02)
    for channel in returnDict['channels']:
        assert channel['name'] == 'testChannel06'
        
def test_invalid_authid():
    clear_v1()
    auth_user_id = 4
    with pytest.raises(AccessError):
        channels_list_v1(auth_user_id)

