import pytest

import jwt
from src.error import AccessError
from src.channels import channels_create_v1, channels_listall_v1
from src.other import clear_v1
from src.auth import auth_register_v1

@pytest.fixture
def token():
    return auth_register_v1("test@unsw.com", 'testPassword8', 'Test', "User")

@pytest.fixture
def names():
    return ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']

@pytest.fixture
def clear():
    clear_v1()

##create one channel with one member and
#  no messages and
def test_oneChannel(clear, token):
    channels_create_v1(token, 'testChannel01', False)
    channelDict = channels_listall_v1(token)
    assert len(channelDict['channels']) == 1
    clear_v1() 
    
##test if there are no channels
def test_noChannels(clear, token):
    assert channels_listall_v1(token) == {'channels': []}
    clear_v1() 

##test with multiple channels and public to true
##test with multiple channels 
def test_fiveChannels_public(clear, token, names):
    for name in names:
        channels_create_v1(token, name, True)
    channelDict = channels_listall_v1(token)
    assert len(channelDict['channels']) == 5
    clear_v1() 
    
##test with multiple channels 
def test_fiveChannels(clear, token, names):
    for values in names:
        channels_create_v1(token, values, False)
    channelDict = channels_listall_v1(token)
    assert len(channelDict['channels']) == 5
    clear_v1() 

def test_invalid_token(clear):
    token = jwt.encode({'test':'token'}, 'testSecret', algorithm='HS256')
    with pytest.raises(AccessError):
        channels_listall_v1(token)
    clear_v1() 
    