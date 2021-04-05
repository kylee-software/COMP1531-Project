import pytest
from src.error import AccessError
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.channel import channel_invite_v1
from src.message import message_send_v2
from src.other import clear_v1, notifications_get_v1
from src.dm import dm_create_v1, dm_invite_v1

@pytest.fixture
def user():
    email = "test1@gmail.com"
    password = "Testtest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v2(email,password,firstname, lastname)


@pytest.fixture
def user2():
    email = "test@gmail.com"
    password = "Testtest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def channel_id(user):
    return channels_create_v2(user['token'], 'channel01', True)['channel_id']

def test_invalid_user():
    with pytest.raises(AccessError):
        notifications_get_v1('falseToken')

def test_return_empty_notifications(clear, user):
    notifications = notifications_get_v1(user['token'])
    assert notifications == {'notifications' : []}

def test_return_single_notification(clear, user, channel_id):
    message_send_v2(user['token'], channel_id, 'Test message @firstname1lastname1')
    notifications = notifications_get_v1(user['token'])
    assert len(notifications['notifications']) == 1

def test_correct_notification_types(clear, user, channel_id):
    message_send_v2(user['token'], channel_id, 'Test message @firstname1lastname1')
    notifications = notifications_get_v1(user['token'])
    assert 'channel_id' in notifications['notifications'][0]
    assert 'dm_id' in notifications['notifications'][0]
    assert 'notification_message' in notifications['notifications'][0]

def test_multiple_tagged_only_1_valid(clear, user, channel_id):
    message_send_v2(user['token'], channel_id, 'Test message @firstname1lastname1 @another @attedword @testing @taggedFunction')
    notifications = notifications_get_v1(user['token'])
    assert len(notifications['notifications']) == 1

def test_tag_multiple_people(clear, user, user2, channel_id):
    channel_invite_v1(user['token'], channel_id, user2['auth_user_id'])
    message_send_v2(user['token'], channel_id, 'Test message @firstname1lastname1 @another @firstnamelastname @testing @taggedFunction')
   
    assert len(notifications_get_v1(user['token'])['notifications']) == 1
    assert len(notifications_get_v1(user2['token'])['notifications']) == 2



def test_returns_no_more_than_20_notification(clear, user, channel_id):
    for i in range(30):
        message_send_v2(user['token'], channel_id, f'Test {i} message @firstname1lastname1')
    notifications = notifications_get_v1(user['token'])
    assert len(notifications['notifications']) == 20

def test_channel_invite_notification(clear, user, user2, channel_id):
    channel_invite_v1(user['token'], channel_id, user2['auth_user_id'])
    notifications = notifications_get_v1(user2['token'])
    assert len(notifications['notifications']) == 1

def test_dm_invite_notification(clear, user, user2):
    dm = dm_create_v1(user['token'], [user['auth_user_id']])
    dm_invite_v1(user['token'], dm['dm_id'], user2['auth_user_id'])
    notifications = notifications_get_v1(user2['token'])
    
    assert len(notifications['notifications']) == 1