from src.data import data
from src.error import AccessError, InputError

def check_auth_user_id_v1(auth_user_id):
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


def check_channel_id_v1(channel_id):
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


