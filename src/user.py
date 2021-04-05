from json import load
from src.helper import is_valid_token, load_data, is_valid_user_id
from src.error import AccessError, InputError


def user_profile_v2(token, u_id):
    """Given a valid u_id returns details about the user 

    Args:
        token (str): a jwt encoded dict with keys session_id and user_id
        u_id (int): the users id that the token wants details about

    Raises:
        AccessError: raises if token is invalid
        InputError: raises if user_id is invalid

    Returns:
        {user}: a dictionary with values u_id, email, name_first, name_last and handle_str
    """
    if not is_valid_token(token):
        raise AccessError("Invalid token")
    if not is_valid_user_id(u_id):
        raise InputError("Invalid user_id")

    data = load_data()
    token = is_valid_token(token)
    user = next(user for user in data['users'] if user['user_id'] == u_id)

    return {'user' : {  'u_id' : u_id,
                        'email' : user['email_address'],
                        'name_first' : user['first_name'],
                        'name_last' : user['last_name'],
                        'handle_str' : user['account_handle'],                            
                     }
            }

def users_all_v1(token):
    if not is_valid_token(token):
        raise AccessError("Token is invalid")
    token = is_valid_token(token)
    data = load_data()
    return_list = []
    for user in data['users']:
        if not user['is_removed']:
            return_list.append({'u_id': user['user_id'],
                                'email': user['email_address'],
                                'name_first': user['first_name'],
                                'name_last': user['last_name'],
                                'handle_str': user['account_handle'],
                                })
    return {'users' : return_list}

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }