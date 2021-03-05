from src.data import data
from src.error import AccessError, InputError

def channel_invite_v1(auth_user_id, channel_id, u_id):
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
    global data
    # First check will be to make sure channel_id is valid
    found_channel_id = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            found_channel_id == True
            break
    if found_channel_id == False:
        raise InputError
    
    # Next we find out if the auth_user_id user is a global owner
    global_status = False
    for user in data['users']:
        if user['user_id'] == auth_user_id:
            global_status == user['global_owner_status']
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
            if global_status == True or is_public == True:
                user_dict = {'user_id':auth_user_id, 'channel_owner_status':global_status,}
                channel['members'].append(user_dict)
            else:
                # If not this means the channel is private and the user doesn't have access
                raise AccessError
            break
    
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }