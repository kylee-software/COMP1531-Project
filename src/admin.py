from src.error import AccessError, InputError
from src.helper import is_valid_channel_id, load_data, save_data, is_valid_token, find_user, is_valid_user_id, \
    is_user_in_channel, is_user_in_dm
from src.channel import channel_removeowner_v1

OWNER_PERMISSION = 1
MEMBER_PERMISSION = 2

def admin_changepermission_v1(token, u_id, permission_id):
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']

    if is_valid_user_id (u_id) == False:
        raise InputError(description=f"invalid u_id: {u_id}")

    if permission_id != OWNER_PERMISSION and permission_id != MEMBER_PERMISSION:
        raise InputError(description=f"invalid permission_id: {permission_id}")

    for user in data['users']:
        if user['user_id'] == auth_user_id:
            user_permission = user['permission_id']
            break
    
    if user_permission != OWNER_PERMISSION:
        raise AccessError(description=f"authorised user is not an owner ")
    
    for user in data['users']:
        if user['user_id'] == u_id:
            user['permission_id'] = permission_id
            break
    save_data(data)

    return {}

def admin_user_remove_v1(token, u_id):
    '''
    Function to remove a user

    Arguments:
        token (string)  - a jwt encoded dict with keys session_id and user_id
        u_id (int)      - the u_id of the user who is being removed from Dreams

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user
                    - Occurs  when user is currently the only owner
        AccessError - Occurs when authorised user is not an owner of Dreams
                    - Occurs when the given token is invalid

        Assumptions: - A global owner can remove themself
                     - Other user can not add the "removed user" to a channel or dm later
                     - if the user with u_id is the only owner of a channel, an InputError will be raised
                     - remove dms that the "remover user" are in if the user is the creator
    Return Value:
        Returns {}
    '''

    data = load_data()

    if not is_valid_token(token):
        raise AccessError("Invalid token.")

    owner_id = is_valid_token(token)['user_id']

    user_info = find_user(owner_id, data)
    if user_info['permission_id'] != 1:
        raise AccessError("Not an owner of Dreams.")

    if not is_valid_user_id(u_id):
        raise InputError(f"user id: {u_id} does not refer to a valid user.")

    owner_count = 0
    for user in data['users']:
        if user['permission_id'] == 1:
            owner_count += 1

    if owner_count == 1:
        raise InputError("User is the only owner of Dreams and can not be removed.")
    else:
        # Update information in 'users':{}
        for user in data['users']:
            if user['user_id'] == u_id:
                user['first_name'] = "Removed"  # f'{name_first}{name_last}' == 'Removed user'
                user['last_name'] = "user"
                user['is_removed'] = True
                if user['permission_id'] == 1:
                    user['permission_id'] = 2
                break

    # search through the channels the user with u_id is in
    for channel in data['channels']:
        if is_user_in_channel(channel['channel_id'], u_id, data):
            # remove the user from the channel the user is in
            for member in channel['members']:
                if member['user_id'] == u_id:
                    if member['permission_id'] == 1:
                        channel_removeowner_v1(token, channel['channel_id'], u_id)
                    channel['members'].remove(member)
                    break

            # replace contents of the messages the user sent with "Removed user"
            for message in channel['messages']:
                if message['message_author'] == u_id:
                    message['message'] = "Removed user"

    # search through the dms the user with u_id is in
    for dm in data['dms']:
        if is_user_in_dm(dm['dm_id'], u_id, data):
            # delete the dm if the "removed user" is the creator
            if dm['creator'] == u_id:
                data['dms'].remove(dm)
            else:
                # remove the user from the dm the user is in
                for member in dm['members']:
                    if member['user_id'] == u_id:
                        dm['members'].remove(u_id)
                        break

                # replace contents of the messages the user sent with "Removed user"
                for message in dm['messages']:
                    if message['message_author'] == u_id:
                        message['message'] = "Removed user"

    save_data(data)
    return {}