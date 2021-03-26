from src.helper import is_valid_user_id, is_valid_channel_id, hash_password, create_token, is_valid_token
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import AccessError, InputError
import pytest
from src.channels import channels_create_v1


def test_invalid_user_id():
    clear_v1()
    assert is_valid_user_id(1) == False

def test_valid_user_id():
    clear_v1()
    user_id = auth_register_v1("test@gmail.com", "password", "first", "last")['auth_user_id']
    assert is_valid_user_id(user_id) == True

def test_invalid_channel_id():
    clear_v1()
    assert is_valid_channel_id(1) == False

def test_valid_channel_id():
    clear_v1()
    user_id = auth_register_v1("test@gmail.com", "password", "first", "last")['auth_user_id']
    channel_id = channels_create_v1(user_id, "Channelname", True)['channel_id']
    assert is_valid_channel_id(channel_id) == True

def test_hash_changes_password():
    assert hash_password('testerpassword') == '9CD2270EA41352837A5A1F0A0ADF1855AB1134C8711B404DB2BB6E7596E62AF2'.lower()


def test_token_create():
    assert create_token(1,1) == 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJzZXNzaW9uX2lkIjoxfQ.in5_bH0KmNeFro-B-Ujxra0Zx5DVTOjGCjjo1Q4T1ls'

def test_invalid_token():
    bad_token = create_token(2,1)
    assert is_valid_token(1, bad_token) == False
    
def test_valid_token():
    good_token = create_token(1,1)
    assert is_valid_token(1, good_token) == True

