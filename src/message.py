from src.data import data
from src.helper import valid_token, get_user_from_token
from src.error import AccessError, InputError
from datetime import datetime
def message_send_v1(token, channel_id, message):
    global data
    if not valid_token(token):
        raise AccessError('Unauthorised User')
    
    if len(message) > 1000:
        raise InputError('Message is longer than 1000 characters')

    user_id = get_user_from_token(token)
    new_message = {'message_id' : data['msg_id_counter'] + 1, 'message_author' : user_id,
                        'message' : message, "time_created" : datetime.now()}

    found_user = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in channel['users']:
                if user['user_id'] == user_id:
                    found_user = True
                    channel['messages'].append(new_message)
    if not found_user:
        raise AccessError('You have not joined this channel')

    data['msg_id_counter'] += 1

    return data['msg_id_counter']

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }