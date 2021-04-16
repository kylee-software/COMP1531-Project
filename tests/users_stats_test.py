import pytest
from src.error import AccessError
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channel import channel_invite_v1, channel_create_v2
from src.dm import dm_create_v1, dm_remove_v1
from src.message import message_senddm_v1, message_send_v2
from src.user import users_stats_v1

@pytest.fixture
def user1():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user2():
    email = "testemail2@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def creator():
    email = "channelcreator@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def channel():
    name = "channel"
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")

    channel_id = channels_create_v2(owner['token'], name, True)['channel_id']
    channel_invite_v1(owner['token'], channel_id, user1['auth_user_id'])
    return channel_id

@pytest.fixture
def dm():
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")
    return dm_create_v1(owner['token'], [user1['auth_user_id']])

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear, user2, channel):
    with pytest.raises(AccessError):
        users_stats_v1('bad.token.input')

def test_all_stats_zero(clear, user2):
    assert users_stats_v1(user2['token']) ==  
                {
                    'channels_exist': [], 
                    'dms_exist': [], 
                    'messages_exist': [], 
                    'utilization_rate':0,
                }

def test_channel_stat(clear, user2, channel):
    stats = users_stats_v1(user2['token'])
    assert len(stats['channels_exist']) == 1
    assert len(stats['dms_exist']) == 0
    assert len(stats['messages_exist']) == 0
    assert stats['utilization_rate'] == 2/3


def test_dm_stat(clear, user2, channel, dm):
    stats = users_stats_v1(user2['token'])
    assert len(stats['channels_exist']) == 1
    assert len(stats['dms_exist']) == 1
    assert len(stats['messages_exist']) == 0
    assert stats['utilization_rate'] == 2/3
    
    # Test again after removing the dm
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    dm_remove_v1(owner['token'], dm['dm_id'])
    stats = users_stats_v1(user2['token'])
    assert len(stats['channels_exist']) == 1
    assert len(stats['dms_exist']) == 0
    assert len(stats['messages_exist']) == 0
    assert stats['utilization_rate'] == 2/3

def test_message_stat(clear, user2, channel, dm):
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    message_senddm_v1(owner['token'], dm['dm_id'], "Message1")
    message = message_send_v2(owner['token'], channel['channel_id'], "message2")
    
    stats = users_stats_v1(user2['token'])
    assert len(stats['channels_exist']) == 1
    assert len(stats['dms_exist']) == 1
    assert len(stats['messages_exist']) == 2
    assert stats['utilization_rate'] == 2/3

    # Check removing dm doesnt change message count
    dm_remove_v1(owner['token'], dm['dm_id'])
    stats = stats = users_stats_v1(user2['token'])
    assert len(stats['messages_exist']) == 2

    # Check removing messafe doesnt change the message count
    message_remove_v1(owner['token'], message['message_id'])
    stats = stats = users_stats_v1(user2['token'])
    assert len(stats['messages_exist']) == 2   


    