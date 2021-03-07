from src.data import data
from src.error import AccessError, InputError
from src.helper import check_auth_user_id_v1 as check_user_id
from src.helper import check_channel_id_v1

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
    
    global data
    # First check will be to make sure channel_id is valid
    check_user_id(auth_user_id)

    check_channel_id_v1(channel_id)
    #found_channel_id = False
    #for channel in data['channels']:
    #    if channel.get('channel_id') == channel_id:
    #        found_channel_id == True
    #        break
    #if found_channel_id == False:
    #    raise InputError(f"channel id: {channel_id} is not a valid channel")
    
    # Next we find out if the auth_user_id user is a global owner
    global_status = 2
    found_user = False
    for user in data['users']:
        if user['user_id'] == auth_user_id:
            global_status == user.get('permission_id')
            found_user = True
            break
    if found_user == False:
        raise InputError(f"user id {auth_user_id} is not a valid user")

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
                raise AccessError(f"channel is private and user is not global owner")
            break
    
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }