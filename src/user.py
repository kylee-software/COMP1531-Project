import re
from src.helper import is_valid_token, load_data, is_valid_user_id, save_data
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