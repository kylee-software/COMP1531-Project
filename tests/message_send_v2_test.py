import pytest
import jwt
import string
import random
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.message import message_send_v2
from src.error import InputError, AccessError
from src.other import clear_v1, notifications_get_v1
from src.helper import load_data, find_user, is_valid_token

@pytest.fixture
def token():
    clear_v1
    email = "test@unsw.au"
    password = "testPassword"
    firstname = "firstName"
    lastname = "lastName"
    return auth_register_v2(email,password,firstname, lastname)['token']

@pytest.fixture
def channel_id(token):
    return channels_create_v2(token, 'testChannel01', False)['channel_id']

@pytest.fixture
def clear():
    clear_v1()


def test_message_too_long(clear, token, channel_id):
    message = ''.join(random.choices(string.ascii_letters, k = 1001))
    with pytest.raises(InputError):
        message_send_v2(token, channel_id, message)

def test_invalid_token(clear, token, channel_id):
    invalid_token = jwt.encode({'test' : 'value'}, 'TestSecret', algorithm='HS256')
    with pytest.raises(AccessError):
        message_send_v2(invalid_token, channel_id, 'testMessage')

def test_user_not_in_channel(clear, token, channel_id):
    second_token = auth_register_v2('test2@unsw.au', 'testPassword', 'secondFirst', 'secondLast')
    with pytest.raises(AccessError):
        message_send_v2(second_token['token'], channel_id, 'testMessage')

def test_message_ids_are_unique(clear, token, channel_id):
    first_id = message_send_v2(token, channel_id, 'testMessaage')['message_id']
    second_id = message_send_v2(token, channel_id, 'secondTestMessage')['message_id']
    assert first_id != second_id

def test_message_with_notification(clear, token, channel_id):
    msg_id = message_send_v2(token, channel_id, 'test message @firstNamelastName')['message_id']
    assert isinstance(msg_id, int)

def test_invalid_channel_id(clear, token):
    with pytest.raises(InputError):
        message_send_v2(token, 'channel_id', 'test message')

def test_notification_message(clear, token, channel_id):
    message = 'test message @firstNamelastName'
    message_send_v2(token, channel_id, message)
    notif = notifications_get_v1(token)
    assert len(notif['notifications']) == 1
    data = load_data()
    channel_name = next(channel['name'] for channel in data['channels'] if channel['channel_id'] == channel_id)
    user_handle = find_user(is_valid_token(token)['user_id'], data)['account_handle']
    assert notif['notifications'][0]['channel_id'] == channel_id
    assert notif['notifications'][0]['dm_id'] == -1
    assert notif['notifications'][0]['notification_message'] == f"{user_handle} tagged you in {channel_name}: {message[:20]}"