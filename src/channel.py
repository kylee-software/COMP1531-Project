from src.error import AccessError, InputError
from src.helper import invite_notification_message, is_valid_user_id, find_user 
from src.helper import is_valid_channel_id, load_data, save_data, is_valid_token

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
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(description=f"Auth_user_id: {auth_user_id} is invalid")

    if is_valid_user_id (u_id) == False:
        raise InputError(description=f"invalid u_id: {u_id}")

    if is_valid_channel_id(channel_id) == False:
        raise InputError(description=f"Channel_id: {channel_id} is invalid")
            
    #check auth_user is in channel
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
            channel['members'].append({'user_id':u_id, 'permission_id':global_owner})
            #notification message
            channel_name = channel_details_v1(token, channel_id)['name']
            invited_user['notifications'].insert(0, invite_notification_message(token_data, channel_id, channel_name, True))
    

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
    
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(description=f"Auth_user_id: {auth_user_id} is invalid")
    
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
                raise AccessError(description=f"auth_user_id is not a channel member")
            
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

    channel
    save_data(data)
    return {
        'name': channel_name,
        'is_public': public_status,
        'owner_members': owner_details,
        'all_members': member_details,
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

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
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(description=f"Auth_user_id: {auth_user_id} is invalid")
    
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
                raise AccessError(description=f"user is not a member of this channel")
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
    
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(description=f"Auth_user_id: {auth_user_id} is invalid")
    
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
                user_dict = {'user_id':auth_user_id, 'permission_id':global_status,}
                channel['members'].append(user_dict)
            else:
                # If not this means the channel is private and the user doesn't have access
                raise AccessError(description=f"channel is private and user is not global owner")
            break
    
    save_data(data)
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }