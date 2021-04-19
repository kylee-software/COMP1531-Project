import pytest
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channel import channel_invite_v1, channel_details_v1
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.message import message_share_v1, message_senddm_v1, message_send_v2
from src.dm import dm_create_v1

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
def OGchannel():
    name = "OGchannel"
    owner = auth_login_v2("channelcreator@gmail.com", "TestTest2")
    user1 = auth_login_v2("testemail@gmail.com", "TestTest")

    channel_id = channels_create_v2(owner['token'], name, True)['channel_id']
    channel_invite_v1(owner['token'], channel_id, user1['auth_user_id'])
    return channel_id

@pytest.fixture
def share_channel():
    name = "Sharechannel"
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

#Where applicable for invalid cases a base case of sharing a message from OGchannel to share_channel will be used

def test_invalid_token(clear, creator, user1, OGchannel, share_channel):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    with pytest.raises(AccessError):
        message_share_v1('bad.token.input', OGmessage, "additional message", share_channel, -1)

def test_invalid_og_message_id(clear, creator, user1, OGchannel, share_channel):
    bad_message = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id'] + 1
    with pytest.raises(InputError):
        message_share_v1(user1['token'], bad_message, "additional message", share_channel, -1)

def test_message_too_long(clear, creator, user1, OGchannel, share_channel):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    with pytest.raises(InputError):
        message_share_v1(user1['token'], OGmessage, "toolong"*1000, share_channel, -1)

def test_invalid_channel_id(clear, creator, user1, OGchannel, share_channel):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    with pytest.raises(InputError):
        message_share_v1(user1['token'], OGmessage, "additional mesage", share_channel + 1, -1)

def test_invalid_dm_id(clear, creator, user1, OGchannel, dm):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    with pytest.raises(InputError):
        message_share_v1(user1['token'], OGmessage, "additional mesage", -1, dm['dm_id'] + 1)

def test_dm_not_1(clear, creator, user1, OGchannel, share_channel):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    with pytest.raises(InputError):
        message_share_v1(user1['token'], OGmessage, "additional mesage", share_channel, 0)

def test_channel_not_1(clear, creator, user1, OGchannel, dm):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    with pytest.raises(InputError):
        message_share_v1(user1['token'], OGmessage, "additional mesage", 0, dm['dm_id'])

def test_user_not_in_OGchannel(clear, creator, user1, OGchannel, share_channel, user2):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    channel_invite_v1(creator['token'], share_channel, user2['auth_user_id'])
    with pytest.raises(AccessError):
        message_share_v1(user2['token'], OGmessage, "additional mesage", share_channel, -1)

def test_user_not_in_OGdm(clear, creator, user1, share_channel, dm, user2):
    OGmessage = message_senddm_v1(creator['token'], dm['dm_id'], "TestMessage")['message_id']
    channel_invite_v1(creator['token'], share_channel, user2['auth_user_id'])
    with pytest.raises(AccessError):
        message_share_v1(user2['token'], OGmessage, "additional mesage", share_channel, -1)

def test_user_not_in_sharechannel(clear, creator, user1, OGchannel, share_channel, user2):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    channel_invite_v1(creator['token'], OGchannel, user2['auth_user_id'])
    with pytest.raises(AccessError):
        message_share_v1(user2['token'], OGmessage, "additional mesage", share_channel, -1)

def test_user_not_in_sharedm(clear, creator, user1, OGchannel, dm, user2):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    channel_invite_v1(creator['token'], OGchannel, user2['auth_user_id'])
    with pytest.raises(AccessError):
        message_share_v1(user2['token'], OGmessage, "additional mesage", -1, dm['dm_id'])

def test_share_to_channel(clear, creator, user1, OGchannel, share_channel):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    assert isinstance(message_share_v1(user1['token'], OGmessage, "additional mesage", share_channel, -1)['shared_message_id'], int)

def test_share_to_dm(clear, creator, user1, OGchannel, dm):
    OGmessage = message_send_v2(creator['token'], OGchannel, "TestMessage")['message_id']
    message = message_share_v1(user1['token'], OGmessage, "additional mesage", -1, dm['dm_id'])['shared_message_id']
    assert isinstance(message, int)
    clear_v1()
