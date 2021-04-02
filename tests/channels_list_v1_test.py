import pytest

from src.channels import channels_create_v1, channels_list_v1
from src.auth import auth_register_v1
from src.error import AccessError
from src.other import clear_v1

@pytest.fixture
def token():
    return auth_register_v1("test@unsw.com", 'testPassword8', 'Test', "User")

@pytest.fixture
def names():
    return ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']

@pytest.fixture
def clear():
    clear_v1()

def test_no_channels(clear, token):
    returnDict = channels_list_v1(token)
    assert returnDict['channels'] == []
    clear_v1() 

def test_lists_a_single_channel(clear,token):
    channels_create_v1(token, 'testChannel01', False)
    returnDict = channels_list_v1(token)
    assert len(returnDict['channels']) == 1
    clear_v1() 

def test_can_see_five_channels(clear, token, names):
    for name in names:
        channels_create_v1(token, name, False)
    returnDict = channels_list_v1(token)
    assert len(returnDict['channels']) == 5
    clear_v1() 

def test_can_only_see_one_of_six(clear, token, names):
    token2 = auth_register_v1("test02@unsw.com", 'testPassword16', 'Test02', "User")]
    for name in names:
        channels_create_v1(token, name, False)
    channels_create_v1(token2, 'testChannel06', False)
    returnDict = channels_list_v1(token2)
    for channel in returnDict['channels']:
        assert channel['name'] == 'testChannel06'
    clear_v1() 
        
def test_invalid_token(clear):
    token = 4
    with pytest.raises(AccessError):
        channels_list_v1(token)
    clear_v1() 

