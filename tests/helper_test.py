from src.helper import check_auth_user_id_v1, check_channel_id_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import AccessError, InputError
import pytest


def test_invalid_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        check_auth_user_id_v1(1)

def test_valid_user_id():
    clear_v1()
    user_id = auth_register_v1("test@gmail.com", "password", "first", "last")['auth_user_id']
    assert check_auth_user_id_v1(user_id) == None


