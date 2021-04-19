from os import access
from src.other import clear_v1
import pytest
from src.error import AccessError, InputError
from src.standup import standup_send_v1, standup_start_v1
import random
import string
from src.auth import auth_register_v2
from src.channels import channels_create_v2
import time
from src.channel import channel_messages_v2

@pytest.fixture
def token():
    return auth_register_v2("test@unsw.com", 'testPassword8', 'Test', "User")['token']

@pytest.fixture
def channel_id(token):
    return channels_create_v2(token, 'testChannel01', False)['channel_id']

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear, token, channel_id):
    standup_start_v1(token, channel_id, 2)
    with pytest.raises(AccessError):
        standup_send_v1('token', channel_id, 'Hello There')

def test_invalid_channel_id(clear, token, channel_id):
    standup_start_v1(token, channel_id, 2)
    with pytest.raises(InputError):
        standup_send_v1(token, 'invalid_channel_id', 'Hello There')

def test_message_more_than_1000(clear, token, channel_id):
    message = ''.join(random.choices(string.ascii_letters, k = 1001))
    standup_start_v1(token, channel_id, 2)
    with pytest.raises(InputError):
        standup_send_v1(token, channel_id, message)

def test_no_active_standup(clear, token, channel_id):
    with pytest.raises(InputError):
        standup_send_v1(token, channel_id, 'Hello There')

def test_user_not_in_channel(clear, token, channel_id):
    token2 = auth_register_v2("test44@unsw.com", 'testPassword8', 'Test44', "User")['token']
    standup_start_v1(token, channel_id, 2)
    with pytest.raises(AccessError):
        standup_send_v1(token2, channel_id, 'Hello There')

def test_everything_valid(clear, token, channel_id):
    standup_start_v1(token, channel_id, 2)
    standup_send_v1(token, channel_id, 'Hello There')
    time.sleep(5)
    assert len(channel_messages_v2(token, channel_id, 0)['messages']) == 1

def test_multiple_messages_are_one(clear, token, channel_id):
    standup_start_v1(token, channel_id, 2)
    standup_send_v1(token, channel_id, 'Hello There')
    standup_send_v1(token, channel_id, 'Hello There1')
    standup_send_v1(token, channel_id, 'Hello There2')
    time.sleep(5)
    print(channel_messages_v2(token, channel_id, 0)['messages'][0]['message'])
    assert len(channel_messages_v2(token, channel_id, 0)['messages']) == 1