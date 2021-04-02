import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channels import channels_create_v1

@pytest.fixture
def user1():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def channel_id():
    name = "Testchannel"
    owner = auth_register_v2("channelcreator@gmail.com", "TestTest1", "first", "last")
    return channels_create_v1(owner['token'], name, True)['channel_id']

@pytest.fixture
def channel_owner():
    return auth_login_v2("channelcreator@gmail.com", "TestTest1")

@pytest.fixture
def clear():
    clear_v1()

def test_channel_leave(clear, channel_id, channel_owner):
    resp = request.post(config.url + 'channel/leave/v1', json={'token': channel_owner['token'], 'channel_id':channel_id})
    assert json.loads(resp.text) == {}

def test_channel_leave_input_error(clear, channel_id, channel_owner):
    resp = request.post(config.url + 'channel/leave/v1', json={'token': channel_owner['token'], 'channel_id':channel_id + 1})
    assert resp.status_code == 400

def test_channel_leave_access_error(clear, channel_id, user1):
    resp = request.post(config.url + 'channel/leave/v1', json={'token': user1['token'], 'channel_id':channel_id + 1})
    assert resp.status_code == 400
    clear_v1()

