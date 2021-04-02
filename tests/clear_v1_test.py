import pytest

from src.auth import auth_register_v2, auth_login_v2
from src.channels import channels_create_v2, channels_listall_v1
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
    auth_user_id = auth_login_v2(
        "test@unsw.au", "testPassword8")['auth_user_id']
    channels_create_v2(auth_user_id, 'testChannel', False)
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v1(auth_user_id) == []
