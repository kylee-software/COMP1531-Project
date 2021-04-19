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
        standup_active_v1('invalid_token', channel_id)

def test_invalid_channel_id(clear, token):
    with pytest.raises(InputError):
        standup_active_v1(token, 'invalid_channel_id')
    pass

def test_standup_running(clear, token, channel_id):
    standup_start_v1(token, channel_id, 5)
    assert standup_active_v1(token, channel_id)['is_active'] == True

def test_returns_false(clear, token, channel_id):
    assert standup_active_v1(token, channel_id)['is_active'] == False
    assert standup_active_v1(token, channel_id)['time_finish'] == None