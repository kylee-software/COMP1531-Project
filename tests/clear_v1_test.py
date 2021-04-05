import pytest

from src.auth import auth_register_v2, auth_login_v2
from src.channels import channels_create_v2, channels_listall_v2
from src.other import clear_v1
from src.error import InputError, AccessError


def test_one_user():
    auth_register_v2("test@unsw.au", "testPassword8", "Test", "User")
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v2("test@unsw.au", "testPassword8")
    # test that auth_login_v1 fails


def test_one_channel():
    clear_v1()
    auth_register_v2("test@unsw.au", "testPassword8", "Test", "User")
    token = auth_login_v2(
        "test@unsw.au", "testPassword8")['token']
    channels_create_v2(token, 'testChannel', False)
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v2(token) == []
