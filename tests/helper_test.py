from src.helper import is_valid_user_id, is_valid_channel_id, hash_password, create_token, is_valid_token, load_data, \
    save_data, find_channel, find_user, is_user_in_channel, is_valid_dm_id, find_dm, is_user_in_dm
from src.auth import auth_register_v2, auth_login_v2
from src.other import clear_v1
from src.error import AccessError, InputError
import pytest
from src.channels import channels_create_v2
from src.dm import dm_create_v1
import json
from src.data import dataStore


def test_invalid_user_id():
    clear_v1()
    assert is_valid_user_id(1) == False
    clear_v1()


def test_valid_user_id():
    clear_v1()
    user_id = auth_register_v2(
        "test@gmail.com", "password", "first", "last")['auth_user_id']
    assert is_valid_user_id(user_id) == True
    clear_v1()


def test_invalid_channel_id():
    clear_v1()
    assert is_valid_channel_id(1) == False
    clear_v1()


def test_valid_channel_id():
    clear_v1()
    token = auth_register_v2(
        "test@gmail.com", "password", "first", "last")['token']
    channel_id = channels_create_v2(token, "Channelname", True)['channel_id']
    assert is_valid_channel_id(channel_id) == True
    clear_v1()

def test_invalid_dm_id():
    clear_v1()
    assert is_valid_dm_id(1) == False
    clear_v1()


def test_valid_dm_id():
    clear_v1()
    token = auth_register_v2(
        "test@gmail.com", "password", "first", "last")['token']
    u_id = auth_register_v2(
        "test1@gmail.com", "password", "firstone", "lastone")['auth_user_id']
    dm_id = dm_create_v1(token, [u_id])['dm_id']
    assert is_valid_dm_id(dm_id) == True
    clear_v1()

def test_hash_changes_password():
    auth_register_v2("test@gmail.com",
                     hash_password("password"), "first", "last")
    with pytest.raises(InputError):
        auth_login_v2("test@gmail.com", "password")
    assert auth_login_v2("test@gmail.com", hash_password("password"))


def test_invalid_token():
    assert is_valid_token('asdaadg.adgtehsf.agaegf') == False


"""### This function requires the v2 implementation of auth register to test adequately    
def test_valid_token():
#    user_info = auth_register_v2("test@gmail.com", "password", "first", "last")
#    user_id = user_info['auth_user_id']  
#    token = user_info['token']  
#    assert is_valid_token(token)['user_id'] == user_id
     assert is_valid_token(create_token(1,1)) != False"""


def test_save_incorrect_data():
    with pytest.raises(Exception):
        save_data({'users': 'testing'})


def test_save_correct_data():
    data = {'users': ['testing'], 'channels': [
        'testing'], 'dms': ['testing'], 'msg_counter': 0,
        'dreams_stats': {'channels_exist':[], 
                                        'dms_exist':[], 
                                        'messages_exist':[], 
                                        'utilization_rate':0}}
    save_data(data)
    load_data()
    assert dataStore == data
    clear_v1()


def test_load_incorrect_data():
    with open('src/data.json', 'w') as FILE:
        json.dump("incorrect", FILE)
<<<<<<< HEAD
    load_data()
    assert dataStore == {'users': [], 'channels': [],
                           'dms': [], 'msg_counter': 0}
=======
    assert load_data() == {'users': [], 'channels': [],
                           'dms': [], 'msg_counter': 0,
                           'dreams_stats': {'channels_exist':[], 
                                        'dms_exist':[], 
                                        'messages_exist':[], 
                                        'utilization_rate':0}}
>>>>>>> master
    clear_v1()


def test_find_channel():
    data = {'users': [], 'channels': [
        {'channel_id': 1, 'members': []}, {'channel_id': 2, 'members': []}]}
    channel = find_channel(1, data)
    assert channel == {'channel_id': 1, 'members': []}
    channel['members'].append('test')
    assert data['channels'][0] == {'channel_id': 1, 'members': ['test']}


def test_find_user():
    data = {'users': [{'user_id': 1}, {
        'user_id': 2, 'name': 'test'}], 'channels': []}
    user = find_user(2, data)
    assert user == {'user_id': 2, 'name': 'test'}
    user['name'] = 'changed'
    assert data['users'][1] == {'user_id': 2, 'name': 'changed'}


def test_is_user_in_channel():
    data = {'users': [], 'channels': [{'channel_id': 1, 'members': []},
                                      {'channel_id': 2, 'members': [{'user_id': 1}]}]}
    assert is_user_in_channel(2, 1, data) == True
    assert is_user_in_channel(1, 1, data) == False


def test_find_dm():
    data = {'users': [], 'dms': [
        {'dm_id': 1, 'members': []}, {'dm_id': 2, 'members': []}]}
    dm = find_dm(1, data)
    assert dm == {'dm_id': 1, 'members': []}
    dm['members'].append('test')
    assert data['dms'][0] == {'dm_id': 1, 'members': ['test']}


def test_is_user_in_dm():
    data = {'users': [], 'dms': [{'dm_id': 1, 'creator': 3, 'members': []},
                                      {'dm_id': 2, 'creator': 2, 'members': [1]}]}
    assert is_user_in_dm(2, 1, data) == True
    assert is_user_in_dm(1, 1, data) == False