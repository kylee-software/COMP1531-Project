from src.helper import check_auth_user_id_v1, check_channel_id_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import AccessError, InputError
import pytest
from src.channels import channels_create_v1


def test_invalid_user_id():
    clear_v1()
    assert check_auth_user_id_v1(1) == False

def test_valid_user_id():
    clear_v1()
    user_id = auth_register_v1("test@gmail.com", "password", "first", "last")['auth_user_id']
    assert check_auth_user_id_v1(user_id) == True

def test_invalid_channel_id():
    clear_v1()
    assert check_channel_id_v1(1) == False

def test_valid_channel_id():
    clear_v1()
    user_id = auth_register_v1("test@gmail.com", "password", "first", "last")['auth_user_id']
    channel_id = channels_create_v1(user_id, "Channelname", True)['channel_id']
    assert check_channel_id_v1(channel_id) == True


