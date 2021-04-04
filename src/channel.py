from src.error import AccessError, InputError
from src.helper import is_valid_token, load_data, save_data, is_valid_channel_id, find_channel, is_user_in_channel

def channel_invite_v1(token, channel_id, u_id):
    '''
    Function to invite and add a user of u_id to a channel of channel_id. 

    Arguments:
        token (int)      - user_id of the person already in the channel
        channel_id (int)        - unique channel identifier
        u_id (int)              - user_id of the person being invited to the channel

    Exceptions:
        InputError  - Occurs when channel_id, u_id or token are not valid ids
        AccessError - Occurs when token is not already a member of the channel

    Return Value:
        Returns {} on successfully added u_id to channel_id
    '''
    data = load_data()
    if is_valid_channel_id(channel_id) == False:
        raise InputError(description=f"Channel_id: {channel_id} is invalid")

    if is_valid_token(token) == False:
        raise AccessError(description=f"Auth_user_id: {token} is invalid")
    
    if is_valid_token(u_id) == False:
        raise InputError(description=f"invalid u_id: {u_id}")
        
    #check auth_user is in channel
    auth_in_channel = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['members']:
                if member['user_id'] == token:
                    auth_in_channel = True
                    break
    if auth_in_channel == False:
        raise AccessError(description=f"token was not in channel")

    # check if user being added is global owner
    global_owner = 2
    for user in data['users']:
        if user['user_id'] == u_id:
            global_owner = user['permission_id']
    
    # add if user isnt already in the channel
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['members']:
                if member['user_id'] == u_id:
                    return {}
            channel['members'].append({'user_id':u_id, 'permission_id':global_owner})
    
    save_data(data)
    return {
    }

def channel_details_v1(token, channel_id):
    '''
    channel details returns the name and member details of a channel a user is in

    Arguments:
        token (int)      - user id of the user requesting channel information
        channel_id (int)        - channel_id of the channel details being requested

    Exceptions:
        InputError  - Occurs when channel id is not valid
        AccessError - Occurs when auth user id is not a member of the channel

    Return Value:
        Returns {name, owner_members, all_members} on successful obtaining of channel details
    '''
    
    data = load_data()

    if is_valid_channel_id(channel_id) == False:
        raise InputError(description=f"Channel_id: {channel_id} is invalid")
    if is_valid_token(token) == False:
        raise AccessError(description=f"Auth_user_id: {token} is invalid")
    
    owner_ids = []
    member_ids = []
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            found_member = False
            channel_name = channel['name']

            for member in channel['members']:
                member_ids.append(member['user_id'])
                if member['permission_id'] == 1:
                    owner_ids.append(member['user_id'])
                if member['user_id'] == token:
                    found_member = True
            
            if found_member == False:
                raise AccessError(description="token is not a channel member")
            
            break
    
    owner_details = []
    member_details = []
    for user in data['users']:
        if user['user_id'] in member_ids:
            member =   {
                            'u_id':user['user_id'],
                            "email":user['email_address'],
                            'name_first':user['first_name'],
                            'name_last':user['last_name'],
                            'handle_str':user['account_handle'],
                        }
            member_details.append(member)
        if user['user_id'] in owner_ids:
            owner = {
                        'u_id':user['user_id'],
                        "email":user['email_address'],
                        'name_first':user['first_name'],
                        'name_last':user['last_name'],
                        'handle_str':user['account_handle'],
                    }
            owner_details.append(owner)

    save_data(data)
    return {
        'name': channel_name,
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

    data = load_data()

    if not is_valid_token(token):
        raise AccessError(description="Token is invalid")

    user_id = is_valid_token(token)['user_id']

    # Check valid channel_id
    if not is_valid_channel_id(channel_id):
        raise InputError(description="Channel ID is invalid.")

    if not is_user_in_channel(channel_id, user_id, data):
        raise AccessError(description=f"User is not a member of the channel with channel id {channel_id}")

    channel_info = find_channel(channel_id, data)
    channel_messages = channel_info['messages']
    # Check valid start number
    if start >= len(channel_messages):
        raise InputError(description="Start is greater than the total number of messages in the channel.")

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
    return {
    }

def channel_join_v1(token, channel_id):
    '''
    Channel join adds a user to a channel if they are authorised to join

    Arguments:
        token (int)      - User id of user attempting to join channel
        channel_id (int)    - channel id of channel user is attempting to join
        ...

    Exceptions:
        InputError  - Channel id is not a valid channel, auth user id is not a valid user
        AccessError - Channel id refers to a private channel if user is not a global owner

    Return Value:
        Returns {} on successfully joining a channel
    '''
    
    data = load_data()
    if is_valid_token(token) == False:
        raise AccessError(description=f"Auth_user_id: {token} is invalid")
    
    if is_valid_channel_id(channel_id) == False:
        raise InputError(description=f"Channel_id: {channel_id} is invalid")

    # Next we find out if the token user is a global owner
    global_status = 2
    for user in data['users']:
        if user['user_id'] == token:
            global_status = user.get('permission_id')
            break

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            # Now we check to see if the user is already in the channel
            for member in channel['members']:
                if member['user_id'] == token:
                    # member is already in channel so return as successful
                    return {}
            is_public = channel['public_status']

            # Now if the user is a global owner or the channel is public they can be added
            if global_status == 1 or is_public == True:
                user_dict = {'user_id':token, 'permission_id':global_status,}
                channel['members'].append(user_dict)
            else:
                # If not this means the channel is private and the user doesn't have access
                raise AccessError(description=f"channel is private and user is not global owner")
            break
    
    save_data(data)
    return {
    }

def channel_addowner_v1(token, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(token, channel_id, u_id):
    return {
    }