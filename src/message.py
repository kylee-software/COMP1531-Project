from helper import is_valid_token, save_data, load_data, is_user_in_channel, find_user
from error import AccessError, InputError

def message_send_v1(auth_user_id, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove_v1(token, message_id):
    '''
    Function to remove a message from a channel or a dm.

    Arguments:
        token (string)       - an authorisation hash of the user
        message_id (int)     - the message id of the message that needs to be removed

    Exceptions:
        AccessError  - the message is not sent by this user nor is an owner of the channel/dm this
                       messages is in nor an owner of Dreams
                     - the token is invalid
        InputError   - message id of this message no longer exists

    Assumption:
            - the creator of dms can not remove a message sent by other users in the dm

    Return Value: {}
    '''

    data = load_data()
    channels = data['channels']
    dms = data['dms']
    in_channel = False
    in_dm = False
    valid_sender = False
    is_owner = False

    if not is_valid_token(token):
        raise AccessError("Not an authorised user of Dreams")

    user_id = is_valid_token(token)['user_id']
    global_permission_id = find_user(user_id)['permission_id']

    for channel in channels:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                in_channel = True
                if message['message_author'] == user_id:  # check if user is the sender
                    valid_sender = True
                if user_id in channel['owners']: # check if user is an owner of the channel
                    is_owner = True

    if in_channel and (not valid_sender and not is_owner and global_permission_id != 1):
        raise AccessError("Not the sender nor an owner of the channel the message was sent in nor an owner of Dreams.")
    elif in_channel:
        for channel in channels:
            for message in channel['messages']:
                if message['message_id'] == message_id:
                    channel['messages'].remove(message)
                    return {}
    else:
        for dm in dms:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    in_dm = True
                    if message['message_author'] == user_id:  # check if user is the sender
                        valid_sender = True
                        dm['messages'].remove(message)
                        return{}

    if in_dm and (not valid_sender and global_permission_id != 1):
        raise AccessError("Not the sender nor an owner of Dreams")

    if not in_channel and not in_dm:
        raise InputError("Message no longer exists.")

    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }