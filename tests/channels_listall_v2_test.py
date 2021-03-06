import pytest

import jwt
from src.error import AccessError
from src.channels import channels_create_v2, channels_listall_v2
from src.other import clear_v1
from src.auth import auth_register_v2

@pytest.fixture
def token():
    return auth_register_v2("test@unsw.com", 'testPassword8', 'Test', "User")['token']

@pytest.fixture
def names():
    return ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']

@pytest.fixture
def clear():
    clear_v1()

##create one channel with one member and
#  no messages and
def test_oneChannel(clear, token):
    channels_create_v2(token, 'testChannel01', False)
    channelDict = channels_listall_v2(token)
    assert len(channelDict['channels']) == 1
    
##test if there are no channels
def test_noChannels(clear, token):
    assert channels_listall_v2(token) == {'channels': []}

##test with multiple channels and public to true
##test with multiple channels 
def test_fiveChannels_public(clear, token, names):
    for name in names:
        channels_create_v2(token, name, True)
    channelDict = channels_listall_v2(token)
    assert len(channelDict['channels']) == 5
    
##test with multiple channels 
def test_fiveChannels(clear, token, names):
    for values in names:
        channels_create_v2(token, values, False)
    channelDict = channels_listall_v2(token)
    assert len(channelDict['channels']) == 5

def test_invalid_token(clear):
    token = jwt.encode({'test':'token'}, 'testSecret', algorithm='HS256')
    with pytest.raises(AccessError):
        channels_listall_v2(token)
    
