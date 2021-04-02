from src.helper import is_valid_token, save_data, load_data, find_user, is_valid_user_id
from src.error import InputError, AccessError

def user_profile_v1(auth_user_id, u_id):
    return {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        },
    }

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(token, handle_str):
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(descripton=f"Auth_user_id: {auth_user_id} is invalid")

    if len(handle_str) <= 3 or len(handle_str) >= 20:
        raise InputError(description=f"handle string is incorrect length, must be between 3 and 20 characters")

    for user in data['users']:
        if user['account_handle'] == handle_str:
            raise InputError(description=f"handle string is already taken")
            
    user = find_user(auth_user_id, data)
    user['account_handle'] = handle_str

    save_data(data)
    return {
    }