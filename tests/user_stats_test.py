import pytest
from src.error import AccessError
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channel import (channel_invite_v1, channel_leave_v1,
                        channel_join_v1, channel_addowner_v1)
from src.channels import channels_create_v2
from src.dm import dm_create_v1, dm_remove_v1
from src.message import message_senddm_v1, message_send_v2, message_remove_v1
from src.user import user_stats_v1

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
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def creator():
    email = "channelcreator@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def channel(user1, creator):
    name = "channel"
    creator = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")

    channel_id = channels_create_v2(creator['token'], name, True)['channel_id']
    channel_invite_v1(creator['token'], channel_id, user1['auth_user_id'])
    return channel_id

@pytest.fixture
def dm():
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")
    return dm_create_v1(owner['token'], [user1['auth_user_id']])

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear, user1):
    with pytest.raises(AccessError):
        user_stats_v1('bad.token.input')

def test_all_stats_zero(clear, user1):
    assert user_stats_v1(user1['token']) == {
                                            'channels_joined': [], 
                                            'dms_joined': [], 
                                            'messages_sent': [], 
                                            'involvement_rate':0,
                                            }

def test_channel_invite_join(clear, channel):
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")

    stats = user_stats_v1(user1['token'])
    assert len(stats['channels_joined']) == 1
    assert len(stats['dms_joined']) == 0
    assert len(stats['messages_sent']) == 0
    assert stats['involvement_rate'] == 1


def test_channel_leave_addowner(clear, channel, user2):
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    channel_addowner_v1(owner['token'], channel, user2['auth_user_id'])
    stats = user_stats_v1(user2['token'])
    assert len(stats['channels_joined']) == 1
    assert len(stats['dms_joined']) == 0
    assert len(stats['messages_sent']) == 0
    assert stats['involvement_rate'] == 1

    # Now test once user leaves channel
    channel_leave_v1(user2['token'], channel)
    stats = user_stats_v1(user2['token'])
    assert len(stats['channels_joined']) == 1
    assert stats['involvement_rate'] == 1

def test_dm_create_remove(clear, channel, dm):
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")

    stats = user_stats_v1(user1['token'])
    assert len(stats['channels_joined']) == 1
    assert len(stats['dms_joined']) == 1
    assert len(stats['messages_sent']) == 0
    assert stats['involvement_rate'] == 1
    
    # Test again after removing the dm
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    dm_remove_v1(owner['token'], dm['dm_id'])
    stats = user_stats_v1(user1['token'])
    assert len(stats['dms_joined']) == 1

def test_message_send_senddm_remove(clear, channel, dm):
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    message_senddm_v1(owner['token'], dm['dm_id'], "Message1")
    message = message_send_v2(owner['token'], channel, "message2")
    
    stats = user_stats_v1(owner['token'])
    assert len(stats['channels_joined']) == 1
    assert len(stats['dms_joined']) == 1
    assert len(stats['messages_sent']) == 2
    assert stats['involvement_rate'] == 1

    # Check removing dm doesnt change message count
    dm_remove_v1(owner['token'], dm['dm_id'])
    stats = stats = user_stats_v1(owner['token'])
    assert len(stats['messages_sent']) == 2

    # Check removing messafe doesnt change the message count
    message_remove_v1(owner['token'], message['message_id'])
    stats = stats = user_stats_v1(owner['token'])
    assert len(stats['messages_sent']) == 2 

def test_involvement_rate(clear, channel, dm):
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    message_senddm_v1(owner['token'], dm['dm_id'], "Message1")
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")
    stats = user_stats_v1(user1['token'])
    
    assert stats['involvement_rate'] == 2/3
