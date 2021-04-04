import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.channel import channel_messages_v2
from src.message import message_send_v2
from src.error import InputError, AccessError

@pytest.fixture
def token():
    # create a test user and return auth_id
    email = "testmail@gamil.com"
    password = "Testpass12345"
    token = auth_register_v2(email, password, "firstname", "lastname")['token']
    return token

@pytest.fixture
def channel_id(token):
    # create a public channel and return channel_id
    return channels_create_v2(token, "channelName1", True)['channel_id']

@pytest.fixture
def unauthorised_user():
    email = "testmail2@gamil.com"
    password = "Testpass1234567"
    token = auth_register_v2(email, password, "firstname", "lastname")['token']
    return token

def test_invalid_token(channel_id):
    with pytest.raises(AccessError):
        channel_messages_v2("invalid_token", channel_id, 0)
    clear_v1()

def test_invalid_channel_id(token, channel_id):
    with pytest.raises(InputError):
        channel_messages_v2(token, channel_id + 1, 0)
    clear_v1()

def test_unauthorised_user(unauthorised_user, channel_id):
    # Test an user that does not belong to the channel with the given channel_id
    with pytest.raises(AccessError):
        channel_messages_v2(unauthorised_user, channel_id, 0)
    clear_v1()

def test_invalid_start(token, channel_id):
    # this fail because no message is being sent to the channel yet
    with pytest.raises(InputError):
        channel_messages_v2(token, channel_id, 51)
    clear_v1()

def test_last_message(token, channel_id):
    # Test if end = -1 when there are no more messages to load after the current return
    message_send_v2(token, channel_id, "Hi, everyone!")
    end = channel_messages_v2(token, channel_id, 0)['end']
    assert end == -1
    clear_v1()

def test_more_messages(token, channel_id):
    count = 60
    while count >= 0:
        message_send_v2(token, channel_id, f"{count}")
        count -= 1

    # Test first 50 newest messages
    message_1 = channel_messages_v2(token, channel_id, 0)['messages'][49]['message']
    assert message_1 == "49"
    # Test the first message in the returned message dictionary
    message_2 = channel_messages_v2(token, channel_id, 10)['messages'][0]['message']
    assert message_2 == "9"
    # Test the second message in the returned message dictionary
    message_3 = channel_messages_v2(token, channel_id, 30)['messages'][1]['message']
    assert message_3 == '30'
    # Test the earliest message that was sent to the channel
    message_4 = channel_messages_v2(token, channel_id, 61)['messages'][0]['message']
    assert message_4 == '60'

    clear_v1()

