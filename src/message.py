from src.helper import is_valid_token, return_valid_tagged_handles, load_data, save_data
from src.error import AccessError, InputError
from datetime import datetime


def message_send_v1(token, channel_id, message):
    data = load_data()
    if not is_valid_token(token):
        raise AccessError('Unauthorised User')
    token = is_valid_token(token)
    if len(message) > 1000:
        raise InputError('Message is longer than 1000 characters')
    
    
    channel = next(channel for channel in data['channels'] if channel['channel_id'] == channel_id)
    msg_user = next((user for user in channel['members'] if user['user_id'] == token['user_id']), False)
    if not msg_user:
        raise AccessError('You have not joined this channel')
    else:

        new_message = {'message_id' : data['msg_counter'] + 1, 'message_author' : token['user_id'],
                            'message' : message, "time_created" : datetime.now()}

        tagged_handles = return_valid_tagged_handles(message, channel_id)
        user_handle = next(user['account_handle'] for user in data['users'] if user['user_id'] == token['user_id'])

        if channel.get('messages') == None:
            channel['messages'] = [new_message]
        else:
            channel['messages'].insert(0, new_message)     

        for user in channel['users']:
            if tagged_handles.count(user['account_handle']) != 0:
                notification_message = f"{user_handle} tagged you in {channel['name']}: {message[0:20]}"
                user['notifications'].insert(0, {channel_id, -1, notification_message})

        data['msg_id_counter'] += 1
        save_data(data)
        return data['msg_counter']

    """found_user = False
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
        pass

    data['msg_id_counter'] += 1

    return data['msg_id_counter']"""



def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }