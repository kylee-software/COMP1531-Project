from src.data import data
from src.error import AccessError, InputError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    '''
    channel details returns the name and member details of a channel a user is in

    Arguments:
        auth_user_id (int)      - user id of the user requesting channel information
        channel_id (int)        - channel_id of the channel details being requested

    Exceptions:
        InputError  - Occurs when channel id is not valid
        AccessError - Occurs when auth user id is not a member of the channel

    Return Value:
        Returns {name, owner_members, all_members} on successful obtaining of channel details
    '''
    
    global data

    found_channel_id = False 
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            found_channel_id == True
            break
    if found_channel_id == False:
        raise InputError("Invalid channel id")
    
    found_auth_id = False
    for user in data['users']:
        if user['user_id'] == auth_user_id:
            found_auth_id == True
    if found_auth_id == False:
        raise AccessError(f"Invalid auth_user_id")

    owner_ids = []
    member_ids = []
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            found_member = False
            channel_name = channel['channel_name']

            for member in channel['members']:
                member_ids.append(member['user_id'])
                if member['owner_status'] == True:
                    owner_ids.append(member['user_id'])
                if member['user_id'] == auth_user_id:
                    found_member = True
            
            if found_member == False:
                raise AccessError("auth_user_id is not a channel member")
            
            break
    
    owner_details = []
    member_details = []
    for user in data['users']:
        if user['user_id'] in member_ids:
            member =   {
                            'u_id':user['user_id'],
                            "email":user['email'],
                            'name_first':user['first_name'],
                            'name_last':user['last_name'],
                            'handle_str':user['handle'],
                        }
            member_details.append(member)
        if user['user_id'] in owner_ids:
            owner = {
                        'u_id':user['user_id'],
                        "email":user['email'],
                        'name_first':user['first_name'],
                        'name_last':user['last_name'],
                        'handle_str':user['handle'],
                    }
            owner_details.append(owner)


    
    return {
        'name': name,
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