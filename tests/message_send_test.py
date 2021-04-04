import pytest
import jwt
import string
import random
from src.auth import auth_register_v2
from src.channels import channels_create_v1
from src.message import message_send_v1
from src.error import InputError, AccessError
from src.other import clear_v1

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
    return channels_create_v1(token, 'testChannel01', False)

@pytest.fixture
def clear():
    clear_v1()


def test_message_too_long(clear, token, channel_id):
    message = ''.join(random.choices(string.ascii_letters, k = 1001))
    with pytest.raises(InputError):
        message_send_v1(token, channel_id, message)

def test_invalid_token(clear, token):
    invalid_token = jwt.encode({'test' : 'value'}, 'TestSecret', algorithm='HS256')
    with pytest.raises(AccessError):
        message_send_v1(invalid_token, 1, 'testMessage')

def test_user_not_in_channel(clear, token, channel_id):
    second_token = auth_register_v2('test2@unsw.au', 'testPassword', 'secondFirst', 'secondLast')
    with pytest.raises(AccessError):
        message_send_v1(second_token['token'], channel_id, 'testMessage')

def test_message_ids_are_different(clear, token, channel_id):
    first_id = message_send_v1(token, channel_id, 'testMessaage')
    second_id = message_send_v1(token, channel_id, 'secondTestMessage')
    assert first_id != second_id