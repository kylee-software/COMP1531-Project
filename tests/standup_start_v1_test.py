import pytest
from src.standup import standup_active_v1, standup_start_v1
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.other import clear_v1

@pytest.fixture
def token():
    return auth_register_v2("test@unsw.com", 'testPassword8', 'Test', "User")['token']

@pytest.fixture
def channel_id(token):
    return channels_create_v2(token, 'testChannel01', False)['channel_id']

@pytest.fixture
def clear():
    clear_v1()

def test_invalid_token(clear, channel_id):
    with pytest.raises(AccessError):
        standup_start_v1('invalid_token', channel_id, 1)

def test_invalid_channel_id(clear, token):
    with pytest.raises(InputError):
        standup_start_v1(token, 'invalid_channel_id', 1)

def test_standup_already_running(clear, token, channel_id):
    standup_start_v1(token, channel_id, 1)
    with pytest.raises(InputError):
        standup_start_v1(token, channel_id, 1)

def test_user_not_in_channel(clear, channel_id):
    invalid_token = auth_register_v2("tes2t@unsw.com", 'testPassword8', 'Test2', "User2")['token']
    with pytest.raises(AccessError):
        standup_start_v1(invalid_token, channel_id, 1)

def test_standup_works(clear, token, channel_id):
    standup_start_v1(token, channel_id, 1)
    assert standup_active_v1(token, channel_id)['is_active'] == True