from src.data import data
from src.helper import valid_token, get_user_from_token, get_handle_from_token, return_valid_tagged_handles
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
    
    tagged_handles = return_valid_tagged_handles(message, channel_id)
    user_handle = get_handle_from_token(token)

    found_user = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in channel['users']:
                if user['user_id'] == user_id:
                    found_user = True
                    if channel.get('messages') == None:
                        channel['messages'] = [new_message]
                    else:
                        channel['messages'].insert(0, new_message)
                
    if found_user:
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                for user in channel['users']:
                    for user1 in data['users']:
                        if user['user_id'] == user1['user_id']:
                            if tagged_handles.count(user1['handle']) != 0:
                                notification_message = f"{user_handle} tagged you in {channel['name']}: {message[0:20]}"
                                if user.get['notifications'] == None:
                                    user['notificatiosn'] = [{channel_id, -1, notification_message}]
                                else:
                                    user['notifications'].insert(0, {channel_id, -1, notification_message})
    else:
        raise AccessError('You have not joined this channel')

    data['msg_id_counter'] += 1

    return data['msg_id_counter']



def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }