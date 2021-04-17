from src.error import AccessError, InputError
from src.helper import (find_channel, find_user,
                        find_user_channel_owner_status,
                        invite_notification_message, is_user_in_channel,
                        is_valid_channel_id, is_valid_token, is_valid_user_id, save_data)
from src.data import dataStore


def channel_invite_v1(token, channel_id, u_id):
    '''
    Function to invite and add a user of u_id to a channel of channel_id.

    Arguments:
        auth_user_id (int)      - user_id of the person already in the channel
        channel_id (int)        - unique channel identifier
        u_id (int)              - user_id of the person being invited to the channel

    Exceptions:
        InputError  - Occurs when channel_id, u_id are not valid ids
        AccessError - Occurs when token is invalid, auth_user_id is invalid or is not already a member of the channel

    Return Value:
        Returns {} on successfully added u_id to channel_id
    '''
    data = dataStore
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")

    auth_user_id = token_data['user_id']
    if is_valid_user_id(auth_user_id) == False:
        raise AccessError(
            description=f"Auth_user_id: {auth_user_id} is invalid")

    if is_valid_user_id(u_id) == False:
        raise InputError(description=f"invalid u_id: {u_id}")

    if is_valid_channel_id(channel_id) == False:
        raise InputError(description=f"Channel_id: {channel_id} is invalid")

    # check auth_user is in channel
    auth_in_channel = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['members']:
                if member['user_id'] == auth_user_id:
                    auth_in_channel = True
                    break
    if auth_in_channel == False:
        raise AccessError(description=f"auth_user_id was not in channel")

    # check if user being added is global owner
    global_owner = 2
    for user in data['users']:
        if user['user_id'] == u_id:
            invited_user = user
            global_owner = user['permission_id']

    # add if user isnt already in the channel
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['members']:
                if member['user_id'] == u_id:
                    return {}
            channel['members'].append(
                {'user_id': u_id, 'permission_id': global_owner})
            # notification message
            channel_name = channel_details_v1(token, channel_id)['name']
            invited_user['notifications'].insert(0, invite_notification_message(
                token_data, channel_id, channel_name, True))

    save_data(data)
    return {
    }


def channel_details_v1(token, channel_id):
    '''
    channel details returns the name and member details of a channel a user is in

    Arguments:
        auth_user_id (int)      - user id of the user requesting channel information
        channel_id (int)        - channel_id of the channel details being requested

    Exceptions:
        InputError  - Occurs when channel id is not valid
        AccessError - Occurs when token is invalid or auth user id is not a member of the channel

    Return Value:
        Returns {name, is_public, owner_members, all_members} on successful obtaining of channel details
    '''

    data = dataStore
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")

    auth_user_id = token_data['user_id']
    if is_valid_user_id(auth_user_id) == False:
        raise AccessError(
            description=f"Auth_user_id: {auth_user_id} is invalid")

    if is_valid_channel_id(channel_id) == False:
        raise InputError(description=f"Channel_id: {channel_id} is invalid")

    owner_ids = []
    member_ids = []

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            found_member = False
            channel_name = channel['name']
            public_status = channel['public_status']

            for member in channel['members']:
                member_ids.append(member['user_id'])
                if member['permission_id'] == 1:
                    owner_ids.append(member['user_id'])
                if member['user_id'] == auth_user_id:
                    found_member = True

            if found_member == False:
                raise AccessError(
                    description=f"auth_user_id is not a channel member")

            break

    owner_details = []
    member_details = []
    for user in data['users']:
        if user['user_id'] in member_ids:
            member = {
                'u_id': user['user_id'],
                "email": user['email_address'],
                'name_first': user['first_name'],
                'name_last': user['last_name'],
                'handle_str': user['account_handle'],
            }
            member_details.append(member)
        if user['user_id'] in owner_ids:
            owner = {
                'u_id': user['user_id'],
                "email": user['email_address'],
                'name_first': user['first_name'],
                'name_last': user['last_name'],
                'handle_str': user['account_handle'],
            }
            owner_details.append(owner)

    channel
    save_data(data)
    return {
        'name': channel_name,
        'is_public': public_status,
        'owner_members': owner_details,
        'all_members': member_details,
    }


def channel_messages_v2(token, channel_id, start):
    '''
        Function to return up to 50 messages between "start" and "start + 50"

        Arguments:
            token (string)      - an authorisation hash of the user
            channel_id (int)    - channel_id of the channel the user is trying to access to
            start (int)         - show messages starting from start; start = 0 means the most recent message

        Exceptions:
            AccessError - Occurs when the token is invalid
                        - authorised user is not a member of the channel

            InputError  - Occurs when channel_id is invalid and "start" is greater than\
            the total number of messages in the channel

        Return Value:
            Returns {messages, start, end} where messages is a dictionary
    '''

    data = dataStore

    if not is_valid_token(token):
        raise AccessError(description="Token is invalid")

    user_id = is_valid_token(token)['user_id']

    if not is_valid_channel_id(channel_id):
        raise InputError(description="Channel ID is invalid.")

    channel_info = find_channel(channel_id, data)
    channel_messages = channel_info['messages']

    if not is_user_in_channel(channel_id, user_id, data):
        raise AccessError(
            description=f"User is not a member of the channel with channel id {channel_id}")

    # Check valid start number
    if start >= len(channel_messages) and start != 0:
        raise InputError(
            description="Start is greater than the total number of messages in the channel.")

    # calculate the ending return value
    end = start + 50 if (start + 50 < len(data['channels']) - 1) else -1
    messages_dict = {'messages': [],
                     'start': start,
                     'end': end
                     }

    if end == -1:
        for i in range(start, len(channel_messages)):
            messages_dict['messages'].append(channel_messages[i])
    else:
        for i in range(start, end):
            messages_dict['messages'].append(channel_messages[i])

    save_data(data)
    return messages_dict
    # example
    # {
    #     'messages': [
    #         {
    #             'message_id': 1,
    #             'u_id': 1,
    #             'message': 'Hello world',
    #             'time_created': 1582426789,
    #         }
    #     ],
    #     'start': 0,
    #     'end': 50,
    # }


def channel_leave_v1(token, channel_id):
    '''
    Function to allow a user to leave a channel

    Arguments:
        token (string)       - an authorisation hash of the user
        channel_id (int)     - channel id of the channel the user is leaving

    Exceptions:
        AccessError  - Occurs when the token invalid or when the user is not in the channel
        InputError   - Occurs when channel_id does not refer to a valid channel

    Return Value:
        {} on successful leaving of the channel

    '''
    data = dataStore
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")

    auth_user_id = token_data['user_id']
    if is_valid_user_id(auth_user_id) == False:
        raise AccessError(
            description=f"Auth_user_id: {auth_user_id} is invalid")

    if is_valid_channel_id(channel_id) == False:
        raise InputError(description=f"Channel_id: {channel_id} is invalid")

    found_member = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for idx, member in enumerate(channel['members']):
                if member['user_id'] == auth_user_id:
                    found_member = True
                    del channel['members'][idx]
                    break
            if found_member == False:
                raise AccessError(
                    description=f"user is not a member of this channel")
    save_data(data)

    return {
    }


def channel_join_v1(token, channel_id):
    '''
    Channel join adds a user to a channel if they are authorised to join

    Arguments:
        auth_user_id (int)      - User id of user attempting to join channel
        channel_id (int)    - channel id of channel user is attempting to join
        ...

    Exceptions:
        InputError  - Channel id is not a valid channel, auth user id is not a valid user
        AccessError - Channel id refers to a private channel if user is not a global owner

    Return Value:
        Returns {} on successfully joining a channel
    '''

    data = dataStore
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")

    auth_user_id = token_data['user_id']
    if is_valid_user_id(auth_user_id) == False:
        raise AccessError(
            description=f"Auth_user_id: {auth_user_id} is invalid")

    if is_valid_channel_id(channel_id) == False:
        raise InputError(description=f"Channel_id: {channel_id} is invalid")

    # Next we find out if the auth_user_id user is a global owner
    global_status = 2
    for user in data['users']:
        if user['user_id'] == auth_user_id:
            global_status = user.get('permission_id')
            break

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            # Now we check to see if the user is already in the channel
            for member in channel['members']:
                if member['user_id'] == auth_user_id:
                    # member is already in channel so return as successful
                    return {}
            is_public = channel['public_status']

            # Now if the user is a global owner or the channel is public they can be added
            if global_status == 1 or is_public == True:
                user_dict = {'user_id': auth_user_id,
                             'permission_id': global_status, }
                channel['members'].append(user_dict)
            else:
                # If not this means the channel is private and the user doesn't have access
                raise AccessError(
                    description=f"channel is private and user is not global owner")
            break

    save_data(data)
    return {
    }


def channel_addowner_v1(token, channel_id, u_id):
    data = dataStore
    # Check if channel exists or not
    channel_id_valid = is_valid_channel_id(channel_id)
    if channel_id_valid is False:
        raise InputError(description="Channel doesn't exist.")

    # Check if user exists
    user_exist = find_user(u_id, data)
    if user_exist is None:
        raise InputError(description="User doesn't exist.")

    # Check if member is already an owner
    channel = find_channel(channel_id, data)
    for member in channel['members']:
        if member['user_id'] == u_id:
            if member['permission_id'] == 1:
                raise InputError(description="User is already an owner.")

    # Check if auth_user_id is an owner
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError(description='Invalid Token')

    first_user_owner = find_user(decoded_token['user_id'], data)
    first_user_owner_status = first_user_owner['permission_id']
    owner_channel_status = find_user_channel_owner_status(
        channel_id, first_user_owner['permission_id'], data)

    if first_user_owner_status == 1 or owner_channel_status == 1:
        if is_user_in_channel(channel_id, u_id, data) is True:
            for member in channel['members']:
                if member['user_id'] == u_id:
                    member['permission_id'] = True
                    if not u_id in channel['owner']:
                        channel['owner'].append(u_id)
        else:
            new_owner = {'user_id': u_id, 'permission_id': True}
            channel['members'].append(new_owner)
            channel['owner'].append(u_id)

        save_data(data)
    else:
        raise AccessError(description="Not an owner of this channel.")
    return {
    }


def channel_removeowner_v1(token, channel_id, u_id):
    '''
    channel_removeowner removes user with user id u_id an owner of this channel

    Arguments:
        token (string)      - an authorisation hash of the user who is removing the ownership of the user with u_id
        channel_id (int)    - channel id of the channel the user's ownership is being removed from
        u_id (int)          - user id of the user who is having their ownership taking away

    Exceptions:
        InputError  - Channel id is not a valid channel
                    - User with u_id is not an owner of the channel
                    - User with u_id is the only owner
        AccessError - The authorised user is not an owner of this channel
                    - User is an authorised user but not an owner of the **Dreams**
                    - User is not an authorised user of **Dreams**

    Return Value:
            Returns {}
    '''

    data = dataStore

    if not is_valid_token(token):
        raise AccessError(description="Token is invalid.")

    user_id = is_valid_token(token)['user_id']

    if not is_valid_channel_id(channel_id):
        raise InputError(description="Channel id is invalid")

    user_permission_id = find_user(user_id, data)['permission_id']
    owners = find_channel(channel_id, data)['owner']

    if user_id not in owners and user_permission_id != 1 :
        raise AccessError(description=f"Not an owner of channel {channel_id} nor an owner of Dreams")

    if u_id not in owners:
        raise InputError(description=f"Not an owner of channel {channel_id}")

    if u_id in owners and len(owners) == 1:
        raise InputError(description=f"User with u_id {u_id} is the only owner of channel {channel_id}")

    if user_id in owners or user_permission_id == 1 :
        for channel in data['channels']:
            for member in channel['members']:
                if member['user_id'] == u_id:
                    member['permission_id'] = 2
                    channel['owner'].remove(u_id)
                    break

    save_data(data)
    return {
    }