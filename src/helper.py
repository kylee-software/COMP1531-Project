from src.data import data
import hashlib
import jwt

SECRET = 'WED09B-ECHO'

def is_valid_user_id(auth_user_id):
    '''
    checks the given auth_user_id is valid

    Arguments:
        auth_user_id (int)      - user_id that needs checking

    Exceptions:
        AccessError - Occurs when user id is not valid

    Return Value:
        Returns None if user_id is valid
    '''

    global data
    for user in data['users']:
        if user['user_id'] == auth_user_id:
            return True
    return False


def is_valid_channel_id(channel_id):
    '''
    checks the given channel_id is valid

    Note:
        requires implementation of channels_create_v1 before testing

    Arguments:
        channel_id (int)      - channel_id that needs checking

    Exceptions:
        InputError - Occurs when channel id is not valid

    Return Value:
        Returns None if channel_id is valid
    '''

    global data
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(user_id, session_id):
    return jwt.encode({'user_id':user_id,'session_id': session_id}, SECRET, algorithm='HS256')

def is_valid_token(user_id, token):
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    decoded_user_id = decoded_token['user_id']

    if decoded_user_id == user_id:
        return True
    else:
        return False
