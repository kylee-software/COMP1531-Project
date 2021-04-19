import pytest
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.message import message_sendlater_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from datetime import datetime, timezone
import random, string

@pytest.fixture
def token():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    firstname = "firstName"
    lastname = "lastName"
    return auth_register_v2(email,password,firstname, lastname)['token']

@pytest.fixture
def channel_id(token):
    return channels_create_v2(token, 'testChannel01', False)['channel_id']

@pytest.fixture
def timestamp():
    return datetime.now().replace(tzinfo=timezone.utc).timestamp()

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear, token, channel_id, timestamp):
    with pytest.raises(AccessError):
        message_sendlater_v1("invalid_token", channel_id, 'testMessage', timestamp)

def test_invalid_channel_id(clear, token, channel_id, timestamp):
    with pytest.raises(InputError):
        message_sendlater_v1(token, channel_id + 1, "testMessage", timestamp)

def test_user_not_in_channel(clear, token, channel_id, timestamp):
    second_token = auth_register_v2('test2@unsw.au', 'testPassword', 'secondFirst', 'secondLast')
    with pytest.raises(AccessError):
        message_sendlater_v1(second_token['token'], channel_id, 'testMessage', timestamp)

def test_message_too_long(clear, token, channel_id, timestamp):
    message = ''.join(random.choices(string.ascii_letters, k=1001))
    with pytest.raises(InputError):
        message_sendlater_v1(token, channel_id, message, timestamp)

def test_invalid_time_sent(clear, token, channel_id, timestamp):
    with pytest.raises(InputError):
        message_sendlater_v1(token, channel_id, "messageTest", timestamp - 2.0)

def test_message_send_later(clear, token, channel_id, timestamp):
    message_id = message_sendlater_v1(token, channel_id, "messageTest", timestamp + 2.0)['message_id']
    assert message_id == 1