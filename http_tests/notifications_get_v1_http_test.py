import pytest
from src.error import AccessError
from src import config
import requests
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.channel import channel_join_v1
from src.message import message_send_v1

def test_invalid_token():
    response = requests.get(config.url + '/notificaionts/get/v1', params={'token': {'test' : 'value'}})
    assert response.status_code == 400

def return_empty_notifications():
    email = "test1@gmail.com"
    password = "Test2est1"
    firstname = "first2ame1"
    lastname = "lastn2me1"
    token = auth_register_v2(email,password,firstname, lastname)['token']
    notifications = requests.get(config.url + '/notifications/get/v1', params={'token' : token})
    assert notifications.json() == {'notifications' : []}

def test_return_correct_notification():
    email = "test1@gmail.com"
    password = "Test2est1"
    firstname = "first2ame1"
    lastname = "lastn2me1"
    token1 = auth_register_v2(email,password,firstname, lastname)['token']
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    token2 = auth_register_v2(email,password,firstname, lastname)['token']
    channel_id = channels_create_v2(token1, 'channel01', True)['channel_id']
    channel_join_v1(token2, channel_id)
    message_send_v1(token1, channel_id, 'Test message @testtest2firstname2')
    notifications = requests.get(config.url + '/notifications/get/v1', params={'token': token2})
    assert len(notifications.json()['notifications']) == 1
