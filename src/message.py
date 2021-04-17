from src.helper import is_valid_token, return_valid_tagged_handles, load_data, save_data, find_user, message_notification_message
from src.helper import is_valid_dm_id, find_dm, tag_users, is_user_in_dm, find_message_source, find_message, find_channel, find_dm, is_user_in_channel, is_valid_channel_id
from src.error import AccessError, InputError
from datetime import datetime
from src.channel import channel_details_v1


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
    channel_name = channel_details_v1(token, channel_id)['name']
    if not is_valid_token(token):
        raise AccessError('Unauthorised User')
    token = is_valid_token(token)
    if len(message) > 1000:
        raise InputError('Message is longer than 1000 characters')

    channel = next(
        (channel for channel in data['channels'] if channel['channel_id'] == channel_id), False)
    if not channel:
        raise InputError('Channel does not exist')

    msg_user = next(
        (user for user in channel['members'] if user['user_id'] == token['user_id']), False)
    if not msg_user:
        raise AccessError('You have not joined this channel')
    else:
        new_message = {'message_id': data['msg_counter'] + 1, 'message_author': token['user_id'],
                       'message': message, "time_created": str(datetime.now()), "is_pinned": False}
        channel['messages'].insert(0, new_message)

        auth_messages = next(user['sent_messages']
                             for user in data['users'] if user['user_id'] == token['user_id'])
        auth_messages.insert(0, data['msg_counter'] + 1)

        tagged_handles = return_valid_tagged_handles(message, channel_id)
        for user in channel['members']:
            user = next(
                (member for member in data['users'] if member['user_id'] == user['user_id']), False)
            if user and tagged_handles.count(user['account_handle']) != 0:
                user['notifications'].insert(0, message_notification_message(
                    token, channel_id, channel_name, True, message))

        data['msg_counter'] += 1
        save_data(data)
        return {'message_id': data['msg_counter']}


def message_remove_v1(auth_user_id, message_id):
    return {
    }


def message_edit_v2(token, message_id, message):

    if len(message) > 1000:
        raise InputError(description='Message over 1000 characters.')

    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description='Invalid Token.')

    data = load_data()

    token_user = find_user(decoded_token['user_id'], data)
    is_dreams_owner = token_user['permission_id'] == 1

    source = None
    found_message = None
    for dm in data['dms']:
        for dm_message in dm['messages']:
            if dm_message['message_id'] == message_id:
                if dm['creator'] == decoded_token['user_id'] or dm_message['message_author'] == decoded_token['user_id'] or is_dreams_owner:
                    found_message = dm_message
                    source = dm
                    break
                else:
                    raise AccessError(
                        description='Not authorised to edit message.')
        if found_message is not None:
            break

    if found_message is None:
        for channel in data['channels']:
            for channel_message in channel['messages']:
                if channel_message['message_id'] == message_id:
                    if decoded_token['user_id'] in channel['owner'] or channel_message['message_author'] == decoded_token['user_id'] or is_dreams_owner:
                        found_message = channel_message
                        source = channel
                        break
                    else:
                        raise AccessError(
                            description='Not authorised to edit message.')
            if found_message is not None:
                break

    if found_message is not None:
        if len(message) == 0:
            source['messages'].remove(found_message)
        else:
            found_message['message'] = message
    else:
        raise InputError(description='No message found.')

    save_data(data)


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

    if channel_id == -1 and dm_id == -1:
        raise InputError(description="a channel id or dm id must be input")

    if channel_id != -1 and dm_id != -1:
        raise InputError(description='either channel id or dm id must be -1')

    # make sure OG message id is valid
    message_source = find_message_source(OG_message_id, data)
    if message_source == None:
        raise InputError(description="could not find OG message")

    OG_message = find_message(OG_message_id, data)

    # now check user is in og dm or channel

    if 'channel_id' in message_source:
        user = next(
            (user for user in message_source['members'] if user['user_id'] == auth_user_id), False)
        if user == False:
            raise AccessError(
                description=f'User not in the original dm/channel message is being shared from')
    else:
        user = next(
            (user for user in message_source['members'] if user == auth_user_id), False)
        if user == False and message_source['creator'] != auth_user_id:
            raise AccessError(
                description=f'User not in the original dm/channel message is being shared from')

    if channel_id != -1:
        new_message = message + '\n"""\n' + OG_message + '\n"""\n'
        return message_send_v2(token, channel_id, new_message)

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
        { message_id } on successful leaving of the channel

    '''
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")

    auth_user_id = token_data['user_id']
    auth_user = find_user(auth_user_id, data)

    if len(message) > 1000:
        raise InputError(description=f"message is too long")

    if is_valid_dm_id(dm_id) == False:
        raise InputError(description='dm is invalid')
    dm = find_dm(dm_id, data)

    if is_user_in_dm(dm_id, auth_user_id,  data) == False:
        raise AccessError(
            description='user is not in the dm they are sharing message to')

    message_id = data['msg_counter'] + 1
    new_message = {'message_id': message_id, 'message_author': auth_user_id,
                   'message': message, "time_created": str(datetime.now()), "is_pinned": False}
    dm['messages'].insert(0, new_message)

    # notify tagged users
    user_message = tag_users(message, auth_user['account_handle'], dm_id, -1)
    if user_message:
        user, message = user_message
        user = next(u for u in data['users'] if u['user_id'] == user)
        user['notifications'].insert(0, message)

    auth_user['sent_messages'].append(message_id)
    data['msg_counter'] += 1
    save_data(data)

    return {'message_id': message_id}


def message_pin_v1(token: str, message_id: int) -> dict:
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description="Invalid Token.")

    data = load_data()

    message_found = find_message_source(message_id, data)

    if message_found is None:
        raise InputError(description="Message was not found.")

    for dm in data['dms']:
        for dm_msg in dm['messages']:
            if dm_msg['message_id'] == message_id:

                is_member = False
                for member in dm['members']:
                    if member == decoded_token['user_id']:
                        is_member = True

                is_owner = False
                if dm['creator'] == decoded_token['user_id']:
                    is_owner = True
                    is_member = True

                if is_member is False:
                    raise AccessError(description="Not a member of the DM")

                if is_owner is False:
                    raise AccessError(description="Not a owner of the DM")

                if dm_msg['is_pinned'] is True:
                    raise InputError(description="DM Message already pinned")

                dm_msg['is_pinned'] = True

    for channel in data['channels']:
        for channel_msg in channel['messages']:
            if channel_msg['message_id'] == message_id:

                is_member = False
                for member in channel['members']:
                    if member == decoded_token['user_id']:
                        is_member = True

                is_owner = False
                for owner in channel['owner']:
                    if owner == decoded_token['user_id']:
                        is_owner = True
                        is_member = True

                if is_member is False:
                    raise AccessError(
                        description="Not a member of this channel")

                if is_owner is False:
                    raise AccessError(
                        description="Not an owner of this channel")

                if channel_msg['is_pinned'] is True:
                    raise InputError(
                        description="Channel Message already pinned")

                channel_msg['is_pinned'] = True

    save_data(data)

    return {}


def message_unpin_v1(token: str, message_id: int) -> dict:

    return {}
