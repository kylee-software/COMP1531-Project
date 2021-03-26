from src.data import data


def return_valid_tagged_handles(message, channel_id):
    split_message = message.split()
    handles = []
    for word in split_message:
        if word.startswith('@'):
            handles.append(word.strip('@'))
    real_handles = []
    for handle in handles:
        for user in data['users']:
            if user['handle'] == handle:
                real_handles.append(handle)
    real_handles_in_channel = []
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for handle in real_handles:
                for member in channel['members']:
                    if member['handle'] == handle:
                        real_handles_in_channel.append(handle)
    return real_handles_in_channel

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


