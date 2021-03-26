from src.helper import is_valid_user_id, is_valid_channel_id, hash_password, create_token, is_valid_token, load_data, save_data
from src.auth import auth_register_v1, auth_login_v1
from src.other import clear_v1
from src.error import AccessError, InputError
import pytest
from src.channels import channels_create_v1


def test_invalid_user_id():
    clear_v1()
    assert is_valid_user_id(1) == False
    clear_v1() 

def test_valid_user_id():
    clear_v1()
    user_id = auth_register_v1("test@gmail.com", "password", "first", "last")['auth_user_id']
    assert is_valid_user_id(user_id) == True
    clear_v1() 

def test_invalid_channel_id():
    clear_v1()
    assert is_valid_channel_id(1) == False
    clear_v1() 

def test_valid_channel_id():
    clear_v1()
    user_id = auth_register_v1("test@gmail.com", "password", "first", "last")['auth_user_id']
    channel_id = channels_create_v1(user_id, "Channelname", True)['channel_id']
    assert is_valid_channel_id(channel_id) == True
    clear_v1() 

def test_hash_changes_password():
    auth_register_v1("test@gmail.com", hash_password("password"), "first", "last")
    with pytest.raises(InputError):
        auth_login_v1("test@gmail.com", "password")
    assert auth_login_v1("test@gmail.com", hash_password("password"))


def test_invalid_token():
    assert is_valid_token('asdaadg.adgtehsf.agaegf') == False

### This function requires the v2 implementation of auth register to test adequately    
def test_valid_token():
#    user_info = auth_register_v2("test@gmail.com", "password", "first", "last")
#    user_id = user_info['auth_user_id']  
#    token = user_info['token']  
#    assert is_valid_token(token)['user_id'] == user_id
     assert is_valid_token(create_token(1,1)) != False

def test_load_save_file():
    save_data({})
    assert load_data() == {}
    save_data({'test':'testing'})
    assert load_data() == {'test':'testing'}
