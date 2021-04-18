import re

from src.error import AccessError, InputError
from src.helper import (find_user, is_valid_token, is_valid_user_id, load_data,
                        save_data)


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
        raise AccessError(description="Invalid token")
    if not is_valid_user_id(u_id):
        raise InputError(description="Invalid user_id")

    data = load_data()
    token = is_valid_token(token)
    user = next(user for user in data['users'] if user['user_id'] == u_id)

    return {'user': {'u_id': u_id,
                     'email': user['email_address'],
                     'name_first': user['first_name'],
                     'name_last': user['last_name'],
                     'handle_str': user['account_handle'],
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

def user_profile_setname_v2(token, name_first, name_last):
    token_data = is_valid_token(token)
    if token_data is False:
        raise AccessError(description="Authorised user id invalid.")

    first_name_length = len(name_first)
    last_name_length = len(name_last)
    character_max = 50
    character_min = 1

    if first_name_length <= character_min or first_name_length >= character_max:
        raise InputError(
            description="The length of the first name given has exceeded the limit of 50 characters.")
    elif last_name_length <= character_min or last_name_length >= character_max:
        raise InputError(
            description="The length of the first or last name given has exceeded the limit of 50 characters.")
    else:
        data = load_data()

        user_modified = find_user(token_data['user_id'], data)

        user_modified['first_name'] = name_first
        user_modified['last_name'] = name_last

        save_data(data)

    return {
    }


def user_profile_setemail_v2(token, email):
    '''
    Update the authorised user's email address

    Arguments:
        token (string)    - a jwt encoded dict with keys session_id and user_id
        email (string)    - email address of the user

    Exceptions:
        InputError  - Email entered is not a valid email
                    - Email address is already being used by another user
        AccessError - Token is invalid

    Return Value:
        Returns {}
    '''
    data = load_data()
    if not is_valid_token(token):
        raise AccessError(description="Token is invalid.")

    user_id = is_valid_token(token)['user_id']

    # check if the email is valid
    if re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email) is None:
        raise InputError(description=f"Email {email} is not a valid email.")

    for user in data['users']:
        if user['email_address'] == email:
            raise InputError(
                description="Email address is already being used by another user.")

    # Set email address to the new given email
    for user in data['users']:
        if user['user_id'] == user_id:
            user['email_address'] = email

    save_data(data)


def user_profile_sethandle_v1(token, handle_str):
    data = load_data()
    token_data = is_valid_token(token)
    handle_str = handle_str.lower()
    
    if token_data == False:
        raise AccessError(description=f"Token invalid")

    auth_user_id = token_data['user_id']
    if is_valid_user_id(auth_user_id) == False:
        raise AccessError(
            description=f"Auth_user_id: {auth_user_id} is invalid")

    if len(handle_str) <= 3 or len(handle_str) >= 20:
        raise InputError(
            description=f"handle string is incorrect length, must be between 3 and 20 characters")

    for user in data['users']:
        if user['account_handle'] == handle_str:
            raise InputError(description=f"handle string is already taken")

    user = find_user(auth_user_id, data)
    user['account_handle'] = handle_str

    save_data(data)
    return {
    }

def user_stats_v1(token):
    data = load_data()
    if not is_valid_token(token):
        raise AccessError(description=f"Token invalid")

    user_id = is_valid_token(token)['user_id']    
    user_stats = find_user(user_id, data)['user_stats']
    sum_user = len(user_stats['channels_joined']) + len(user_stats['dms_joined']) + len(user_stats['messages_sent'])
    sum_dreams = len(data['channels']) + len(data['dms']) + data['msg_counter']

    if sum_dreams == 0:
        user_stats['involvement_rate'] = 0
    else:
        user_stats['involvement_rate'] = sum_user/sum_dreams

    return user_stats