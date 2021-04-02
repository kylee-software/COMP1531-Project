from src.helper import is_valid_token, load_data, is_valid_user_id
from src.error import AccessError, InputError


def user_profile_v2(token, u_id):
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

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }