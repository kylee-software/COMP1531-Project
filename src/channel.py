from src.data import data
from src.error import AccessError, InputError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    Function to invite and add a user of u_id to a channel of channel_id. 

    Arguments:
        auth_user_id (int)      - user_id of the person already in the channel
        channel_id (int)        - unique channel identifier
        u_id (int)              - user_id of the person being invited to the channel

    Exceptions:
        InputError  - Occurs when channel_id, u_id or auth_user_id are not valid ids
        AccessError - Occurs when auth_user_id is not already a member of the channel

    Return Value:
        Returns {} on successfully added u_id to channel_id
    '''
    global data
    #check valid channle id
    valid_id = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            valid_id = True
            break
    if valid_id == False:
        raise InputError(f"channel_id: {channel_id} is not valid.")
    
    #check valid u id and auth_u_id
    valid_id = False
    valid_auth_id = False
    for user in data['users']:
        if user['user_id'] == u_id:
            valid_id = True
        if user['user_id'] == auth_user_id:
            valid_auth_id = True
    if valid_id == False:
        raise InputError(f"u_id: {u_id} is not valid")
    if valid_auth_id = False:
        raise InputError(f"auth_user_id: {auth_user_id} is not valid")

    #check auth_user is in channel
    auth_in_channel = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in data['members']:
                if member['user_id'] == auth_user_id:
                    auth_in_channel = True
                    break
    if auth_in_channel == False:
        raise AccessError(f"auth_user_id was not in channel")

    # check if user being added is global owner
    global_owner == 2:
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
    
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
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

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }