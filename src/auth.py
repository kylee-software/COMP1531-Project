import re

from src.error import InputError
from src.helper import save_data, load_data, create_token, hash_password, is_valid_token
import uuid
import jwt
import json
import src.data


class uuidencode(json.JSONEncoder):
    """
        Creation of class to help with the json encoding of UUID
    """

    def default(self, uuid_id):
        if isinstance(uuid_id, uuid.UUID):
            return str(uuid_id)
        return json.JSONEncoder.default(self, uuid_id)


def create_session(user):
    """
    Generates a unique session id, appends it to the user's session list and returns the json encoded uuid.

    Arguments:
        user - element in dictionary - a user's account details

    Return Value:
        Returns unique_id_json after generating a unique session id for the user and appending it to the user's session list.
    """
    unique_id = uuid.uuid4()
    unique_id_json = json.dumps(unique_id, cls=uuidencode)
    user['session_list'].append(unique_id_json)
    return unique_id_json


def auth_login_v2(email, password):
    """
    user_login_v2 takes in an email and password. 
    It checks that the email is a valid format, belongs to a registered user and that the password belongs to the user.
    If conditions are met the user is logged in and the function returns user id.
    Otherwise, an error is raised.

    Arguments:
        email (string) - The email inputted by the user.
        password (string) - The password inputted by the user.

    Exceptions:
        InputError  - Occurs when email does not match valid email format.
        InputError - Occurs when email does not belong to a registered user.
        InputError - Occurs when the password does not belong to the registered user.

    Return Value:
        Returns {'token': login_token, 'auth_user_id': user['user_id']} on the condition that the email is valid, 
        belongs to a registered user and that the password belongs to the registered user.

    """
    data = load_data()
    if re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email) == None:
        raise InputError('Please enter a valid email address.')

    for user in data['users']:
        if user['email_address'] == email:
            hashed_password = hash_password(password)
            if user['account_password'] == hashed_password:
                login_session_id = create_session(user)
                save_data(data)
                login_token = create_token(user['user_id'], login_session_id)
                return {'token': login_token, 'auth_user_id': user['user_id']}
            else:
                raise InputError('Incorrect Password.')
    raise InputError('Email not found.')


def auth_register_v2(email, password, name_first, name_last):
    """
auth_register_v1 is a function that takes in an email, password and a new user's first and last name.
It then checks the email, password, first and last names are all valid.
It then creates a handle for the new user.
For global permissions, the very first user registered is an owner whilst subsequent users are just members.
A dictionary is then created for the new user and appended to the list of users in the global dictionary data.
The function then returns the user id.
Otherwise, an error is raised. 
Please note that currently the handle is not able to be tested in this iteration and will be tested in later iterations. 

Arguments:
    email (string) - The email inputted by the new user.
    password (string) - The password inputted by the new user.
    name_first (string) - The new user's first name.
    name_last (string) - The new user's last name.

Exceptions:
    InputError  - Occurs when email is not a valid format.
    InputError - Occurs when email is already registered by another user.
    InputError - Occurs when password is less than 6 characters long.
    InputError - Occurs when first name is less than 1 character and greater than 50 characters in length.
    InputError - Occurs when last name is less than 1 character and greater than 50 characters in length.
    InputError - Occurs when the handle has either '@' or whitespace.

Return Value:
    Returns {'token': login_token, 'auth_user_id': new_user['user_id']} on the condition that the email is valid and not previously registered.
    Additionally, that the password, first and last names are the correct length.
    Further that the handle has no '@' or whitespace.
    """
    data = load_data()
    password_length = len(password)
    first_name_length = len(name_first)
    last_name_length = len(name_last)

    if re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email) is None:
        raise InputError('Please enter a valid email address.')

    for user in data['users']:
        if user['email_address'] == email:
            raise InputError('Email already registered.')

    if password_length < 6:
        raise InputError('Password is less than 6 characters.')

    if first_name_length < 1 or first_name_length > 50:
        raise InputError('First name is not a valid length.')

    if last_name_length < 1 or last_name_length > 50:
        raise InputError('Last name is not a valid length.')

    handle = name_first + name_last

    for character in handle:
        if character == '@' or character.isspace():
            raise InputError("No @ or whitespace allowed in handles.")

    if len(handle) > 20:
        handle = handle[0:20]
        handle = handle.lower()

    user_list = data['users']
    i = 0
    number = 0
    updated_handle = handle
    while i < len(user_list):
        user = user_list[i]
        if user['account_handle'] == updated_handle:
            updated_handle = handle + str(number)
            i = 0
            number += 1
        i += 1
    permission_id = 2
    if len(data['users']) == 0:
        permission_id = 1
    new_user = {
        'first_name': name_first,
        'last_name': name_last,
        'email_address': email,
        'account_password': hash_password(password),
        'permission_id': permission_id,
        'account_handle': updated_handle,
        'session_list': [],
        'user_id': len(data['users']) + 1,
        'notifications': [],
        'sent_messages': [],
    }
    login_session_id = create_session(new_user)

    user_list.append(new_user)
    save_data(data)

    login_token = create_token(new_user['user_id'], login_session_id)

    return {'token': login_token, 'auth_user_id': new_user['user_id']}


def auth_logout_v1(token):
    """Given an active token, invalidates the token to log the user out. If a 
    valid token is given, and the user is successfully logged out, it returns true, otherwise false.

    Args:
        token (string): encoded jwt 

    Returns:
        boolean: True if successfully logged out, False if otherwise
    """
    if not is_valid_token(token):
        return False
    else: 
        data = load_data()
        decoded_token = is_valid_token(token)
        for user in data['users']:
            if user['session_list'].count(decoded_token['session_id']) != 0:
                user['session_list'].remove(decoded_token['session_id'])
                save_data(data)
                return {'is_success': True}
    return {'is_success': False}
