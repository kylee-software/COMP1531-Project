from src.helper import is_valid_user_id, load_data, save_data, find_user
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


def user_profile_setname_v2(auth_user_id, name_first, name_last):
    if is_valid_user_id(auth_user_id) is False:
        raise AccessError("Authorised user id invalid.")

    first_name_length = len(name_first)
    last_name_length = len(name_last)
    character_max = 50
    character_min = 1

    if first_name_length <= character_min or first_name_length >= character_max:
        raise InputError(
            "The length of the first name given has exceeded the limit of 50 characters.")
    elif last_name_length <= character_min or last_name_length >= character_max:
        raise InputError(
            "The length of the first or last name given has exceeded the limit of 50 characters.")
    else:
        data = load_data()

        user_modified = find_user(auth_user_id, data)

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
