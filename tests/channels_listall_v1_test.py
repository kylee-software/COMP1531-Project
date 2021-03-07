import pytest


from src.error import AccessError
from src.channels import channels_create_v1, channels_listall_v1
from src.other import clear_v1
from src.auth import auth_register_v1

@pytest.fixture
def auth_user_id():
    return auth_register_v1("test@test.unsw.com", 'testPassword8', 'Test', "User")

@pytest.fixture
def names():
    return ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']

##create one channel with one member and
#  no messages and
def test_oneChannel(auth_user_id):
    clear_v1()
    channels_create_v1(auth_user_id, 'testChannel01', False)
    channelDict = channels_listall_v1(auth_user_id)
    assert len(channelDict['channels']) == 1
    
##test if there are no channels
def test_noChannels(auth_user_id):
    clear_v1()
    assert channels_listall_v1(auth_user_id) == {'channels': []}

##test with multiple channels and public to true
##test with multiple channels 
def test_fiveChannels_public(auth_user_id, names):
    clear_v1()
    for name in names:
        channels_create_v1(auth_user_id, name, True)
    channelDict = channels_listall_v1(auth_user_id)
    assert len(channelDict['channels']) == 5
    
##test with multiple channels 
def test_fiveChannels(auth_user_id, names):
    clear_v1()
    for values in names:
        channels_create_v1(auth_user_id, values, False)
    channelDict = channels_listall_v1(auth_user_id)
    assert len(channelDict['channels']) == 5

def test_invalid_authId():
    clear_v1()
    auth_user_id = 4
    with pytest.raises(AccessError):
        channels_listall_v1(auth_user_id)
    