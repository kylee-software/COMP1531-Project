from src.helper import is_valid_token, load_data, is_valid_user_id, save_data, find_user
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

    return {'user': {'u_id': u_id,
                     'email': user['email_address'],
                     'name_first': user['first_name'],
                     'name_last': user['last_name'],
                     'handle_str': user['account_handle'],
                     }
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


def user_profile_setemail_v1(auth_user_id, email):
    return {
    }


def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }
