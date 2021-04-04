import pytest
from src.error import AccessError
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.message import message_send_v2
from src.other import clear_v1
from src.other import notifications_get_v1

@pytest.fixture
def token():
    email = "test1@gmail.com"
    password = "Testtest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v2(email,password,firstname, lastname)['token']

@pytest.fixture
def clear():
    clear_v1()


def test_invalid_token():
    with pytest.raises(AccessError):
        notifications_get_v1('falseToken')

def test_return_empty_notifications(clear, token):
    notifications = notifications_get_v1(token)
    assert notifications == {'notifications' : []}

def test_return_single_notification(clear, token):
    channel_id = channels_create_v2(token, 'channel01', True)['channel_id']
    message_send_v2(token, channel_id, 'Test message @firstname1lastname1')
    notifications = notifications_get_v1(token)
    assert len(notifications['notifications']) == 1

def test_correct_notification_types(clear, token):
    channel_id = channels_create_v2(token, 'channel01', True)['channel_id']
    message_send_v2(token, channel_id, 'Test message @firstname1lastname1')
    notifications = notifications_get_v1(token)
    assert 'channel_id' in notifications['notifications'][0]
    assert 'dm_id' in notifications['notifications'][0]
    assert 'notification_message' in notifications['notifications'][0]

def test_multiple_tagged_only_1_valid(clear, token):
    channel_id = channels_create_v2(token, 'channel01', True)['channel_id']
    message_send_v2(token, channel_id, 'Test message @firstname1lastname1 @another @attedword @testing @taggedFunction')
    notifications = notifications_get_v1(token)
    assert len(notifications['notifications']) == 1

def test_returns_no_more_than_20_notification(clear, token):
    channel_id = channels_create_v2(token, 'channel01', True)['channel_id']
    for i in range(30):
        message_send_v2(token, channel_id, f'Test {i} message @firstname1lastname1')
    notifications = notifications_get_v1(token)
    assert len(notifications['notifications']) == 20

def test_channel_invite_notification(clear, token):
    pass

def test_dm_invite_notification(clear, token):
    pass