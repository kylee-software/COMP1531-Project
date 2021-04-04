from src.helper import is_valid_token, return_valid_tagged_handles, load_data, save_data
from src.error import AccessError, InputError
from datetime import datetime


def message_send_v2(token, channel_id, message):
    """Sends a message from the user referenced by the token to the channel referenced by
    channel_id

    Args:
        token (str): jwt encode dict with keys session_id and user_id
        channel_id (int): id of a channel, may or may not be valid
        message (str): the message to be sent

    Raises:
        AccessError: raised when token is invalid
        InputError: raised when message being sent is longer than 1000 characters
        InputError: raised when channel referenced by channel_id does not exist
        AccessError: raised when the user reference by token is not part of channel
        referenced by channel_id

    Returns:
        int: a unique number identifying the message
    """
    data = load_data()
    if not is_valid_token(token):
        raise AccessError('Unauthorised User')
    token = is_valid_token(token)
    if len(message) > 1000:
        raise InputError('Message is longer than 1000 characters')
    
    
    channel = next((channel for channel in data['channels'] if channel['channel_id'] == channel_id), False)
    if not channel:
        raise InputError('Channel does not exist')

    msg_user = next((user for user in channel['members'] if user['user_id'] == token['user_id']), False)
    if not msg_user:
        raise AccessError('You have not joined this channel')
    else:
        new_message = {'message_id' : data['msg_counter'] + 1, 'message_author' : token['user_id'],
                            'message' : message, "time_created" :str(datetime.now())}
        channel['messages'].insert(0, new_message)     

        tagged_handles = return_valid_tagged_handles(message, channel_id)
        user_handle = next(user['account_handle'] for user in data['users'] if user['user_id'] == token['user_id'])
        for user in channel['members']:
            user = next((member for member in data['users'] if member['user_id'] == user['user_id']), False)
            if user and tagged_handles.count(user['account_handle']) != 0:
                notification_message = f"{user_handle} tagged you in {channel['name']}: {message[:20]}"
                user['notifications'].insert(0, {'channel_id' : channel_id, 'dm_id': -1, 'notification_message': notification_message})

        data['msg_counter'] += 1
        save_data(data)
        return data['msg_counter']

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }