from src.error import AccessError, InputError
from src.helper import load_data, save_data, is_valid_token
import re

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
        raise AccessError("Token is invalid.")

    user_id = is_valid_token(token)['user_id']

    # check if the email is valid
    if re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email) is None:
        raise InputError(f"Email {email} is not a valid email.")

    for user in data['users']:
        if user['email_address'] == email:
            raise InputError("Email address is already being used by another user.")

    # Set email address to the new given email
    for user in data['users']:
        if user['user_id'] == user_id:
            user['email_address'] = email

    save_data(data)

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }