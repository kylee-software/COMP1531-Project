import pytest
from src.standup import standup_active_v1, standup_start_v1
from src.error import AccessError, InputError

def test_invalid_token():
    with pytest.raises(AccessError):
        standup_active_v1('invalid_token', 0)

def test_invalid_channel_id():
    with pytest.raises(InputError):
        standup_active_v1('token', 'invalid_channel_id')
    pass

def test_standup_running():
    standup_start_v1('token', 'channel_id', 0)
    assert standup_active_v1('token', 0)['is_active'] == True

def test_returns_false():
    assert standup_active_v1('tokne', 0)['is_active'] == False
    assert standup_active_v1('token', 0)['time_finish'] == None