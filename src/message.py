from src.helper import is_valid_token, return_valid_tagged_handles, load_data, save_data
from src.helper import find_message, is_valid_channel_id, is_user_in_channel, find_user
from src.helper import is_valid_dm_id, find_dm, tag_users, find_message_source, is_user_in_dm
from src.error import AccessError, InputError
from datetime import datetime


def message_send_v2(token, channel_id, message):
    """Sends a message from the user referenced by the token to the channel referenced by
    channel_id
    Also adds the msg_id to the 'sent_message' list for the user referenced by token and
    add notifications to those users that were mentioned in the message

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

        auth_messages = next(user['sent_messages'] for user in data['users'] if user['user_id'] == token['user_id'])     
        auth_messages.insert(0, data['msg_counter'] + 1)

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

def message_share_v1(token, OG_message_id, message, channel_id, dm_id):
    """Shares a message (OGmessage) from the user referenced by the token to the channel or dm referenced by
    channel_id or dm_id accompanied by an optional message
    Also adds the msg_id to the 'sent_message' list for the user referenced by token and
    add notifications to those users that were mentioned in the message

    Args:
        token (str): jwt encode dict with keys session_id and user_id
        OG_message_id (int): message id of the message to be shared
        dm_id (int): id of a dm
        channel_id (int): id of a channel, may or may not be valid
        message (str): optional additional message to be sent

    Raises:
        AccessError: raised when token is invalid
        InputError: raised when message + message being shared is longer than 1000 characters
        InputError: raised when channel referenced by channel_id does not exist
        InputError: raised when dm referenced by dm_id does not exist
        AccessError: raised when the user reference by token is not part of channel
        referenced by channel_id or the dm referenced by dm_id
        AccessError: raised when the user is not part of the channel or dm the OG message
        is from
        Input Error: raised if the channel_id or dm_id not being shared to is not -1
        Input Error: raised if both channel_id and dm_id are -1 

    Returns:
        int: a unique number identifying the message
    """
    data = load_data()
    if not is_valid_token(token):
        raise AccessError(description='Unauthorised User')
    
    auth_user_id = is_valid_token(token)['user_id']
    auth_user_handle = find_user(auth_user_id, data)['account_handle']

    if channel_id != -1 and dm_id != -1:
        if channel_id == -1 and dm_id == -1:
            raise InputError(description="a channel id or dm id must be input")
        raise InputError(description='either channel id or dm id must be -1')
    
    message_id = data['msg_counter'] + 1
    
    # make sure OG message id is valid
    message_source = find_message_source(OG_message_id, data)
    if message_source == None:
        raise InputError(description="could not find OG message")
    
    OG_message = find_message(OG_message_id, data)
    
    # now check user is in og dm or channel
 
    if 'channel_id' in message_source:
        user = next((user for user in message_source['members'] if user['user_id'] == auth_user_id), False)
        if user == False:
            raise AccessError(description=f'User not in the original dm/channel message is being shared from')
    else:
        user = next((user for user in message_source['members'] if user == auth_user_id), False)
        if user == False and message_source['creator'] != auth_user_id:
            raise AccessError(description=f'User not in the original dm/channel message is being shared from')
    
    if channel_id != -1:
        new_message = message + '\n"""\n' + OG_message + '\n"""\n'
        return {'message_id': message_send_v2(token, channel_id, new_message)}
        
    if dm_id != -1:
        new_message = message + '\n"""\n' + OG_message + '\n"""\n'
        return message_senddm_v1(token, dm_id, new_message)


def message_senddm_v1(token, dm_id, message):
    '''
    Function to send a message to a dm, notifying a user if they are tagged in the message

    Arguments:
        token (string)       - an authorisation hash of the user
        dm_id (int)          - dm id of the dm the user is sending a message to
        message (string)     - message user is sending to the dm

    Exceptions:
        AccessError  - Occurs when the token invalid or when the user is not in the dm
        InputError   - Occurs when dm_id is not a valid dm or when the message is over 1000 characters

    Return Value:
        {} on successful leaving of the channel

    '''
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    auth_user = find_user(auth_user_id, data)
    
    if len(message) > 1000:
        raise InputError(description=f"message is too long")

    if is_valid_dm_id(dm_id, data) == False:
        raise InputError(description='dm is invalid')
    dm = find_dm(dm_id, data)

    if is_user_in_dm(dm_id, auth_user_id,  data) == False:
        raise AccessError(description='user is not in the dm they are sharing message to')
    
    message_id = data['msg_counter'] + 1
    new_message = {'message_id' : message_id, 'message_author' : auth_user_id,
                            'message' : message, "time_created" :str(datetime.now())}
    dm['messages'].insert(0, new_message)
    
    # notify tagged users
    tag_users(message, auth_user['account_handle'], dm_id, -1)
    
    auth_user['sent_messages'].append(message_id)
    data['msg_counter'] += 1

    save_data(data)
    return {'message_id':message_id}
