from os import access
import pytest
from src.error import AccessError
from src import config
import requests
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.channel import channel_join_v1
from src.message import message_send_v1
from src.other import notifications_get_v1

@pytest.fixture
def token():
    email = "test1@gmail.com"
    password = "Test2est1"
    firstname = "first2ame1"
    lastname = "lastn2me1"
    return auth_register_v2(email,password,firstname, lastname)['token']

@pytest.fixture
def token2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)['token']


def test_invalid_token():
    with pytest.raises(AccessError):
        notifications_get_v1('falseToken')

def return_empty_notifications(token):
    notifications = notifications_get_v1(token)
    assert notifications == {'notifications' : []}

def test_return_single_notification(token, token2):
    channel_id = channels_create_v2(token, 'channel01', True)['channel_id']
    channel_join_v1(token2, channel_id)
    message_send_v1(token, channel_id, 'Test message @testtest2firstname2')
    notifications = notifications_get_v1(token)
    assert len(notifications['notifications']) == 1

def test_returns_no_more_than_20_notification(token, token2):
    channel_id = channels_create_v2(token, 'channel01', True)['channel_id']
    channel_join_v1(token2, channel_id)
    for i in range(30):
        message_send_v1(token, channel_id, f'Test {i} message @testtest2firstname2')
    notifications = notifications_get_v1(token)
    assert len(notifications['notifications']) == 20