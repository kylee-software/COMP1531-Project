
from src.helper import load_data, save_data, is_valid_token
from src.error import AccessError, InputError


def clear_v1():
    """empties the data dictionary
    """
    save_data({'users': [], 'channels': [], 'dms': [], 'msg_counter': 0})


def search_v2(token, query_str):
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description='Not authorised to search.')

    if len(query_str) > 1000:
        raise InputError(description='Query string too long.')
    messages = []

    data = load_data()

    for channel in data['channels']:
        is_in_channel = False
        for member in channel['members']:
            if member['user_id'] == decoded_token['user_id']:
                is_in_channel = True
                break
        if decoded_token['user_id'] in channel['owner']:
            is_in_channel = True
        if is_in_channel:
            for channel_message in channel['messages']:
                if query_str in channel_message['message']:
                    messages.append(channel_message)

    for dm in data['dms']:
        is_in_dm = False
        if decoded_token['user_id'] in dm['members']:
            is_in_dm = True
        if dm['creator'] == decoded_token['user_id']:
            is_in_dm = True
        if is_in_dm:
            for dm_message in dm['messages']:
                if query_str in dm_message['message']:
                    messages.append(dm_message)

    return {
        'messages': messages
    }


def notifications_get_v1(token):
    if not is_valid_token(token):
        raise AccessError("Invalid Token")
    token = is_valid_token(token)
    data = load_data()
    user = next(user for user in data['users']
                if user['user_id'] == token['user_id'])
    return {'notifications': user['notifications'][:20]}
