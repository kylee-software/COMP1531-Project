from src.error import InputError, AccessError
from src.helper import is_valid_token, save_data, load_data, is_valid_user_id, find_user

def dm_invite(token, dm_id, user_id):
    if not is_valid_token(token):
        raise AccessError("Invalid Token")
    token = is_valid_token(token)
    data = load_data()

    dm = next((dm for dm in data['dms'] if dm['dm_id'] == dm_id), False)
    if not dm:
        raise InputError("Invalid dm_id")

    if not is_valid_user_id(user_id):
        raise InputError("User you are trying to add doesn't exist")

    if dm['members'].count(user_id) != 0:
        raise InputError("The user you are trying to add is already a part of that dm")
    
    if dm['members'].count(token['user_id']) == 0:
        raise AccessError("Authorised user is not a part of this dm")

    token_user = find_user(token['user_id'], data)
    user = next(user for user in data['users'] if user['user_id'] == user_id)
    user['notifications'].insert(0, {"channel_id": -1, "dm_id": dm_id, "notification_message": f"{token_user['account_handle']} added you to {dm['name']}" })

    dm['members'].append(user_id)
    save_data(data)

    return {}

def dm_create_v1(token, u_ids):
    '''
    Function to create a channel that is either a public or private with a given name

    Arguments:
        token (string)       - an authorisation hash of the user
        u_ids (int [])       - user id of the users that this DM is directed to (excluding the creator)

    Exceptions:
        AccessError  - Occurs when the token invalid
        InputError   - Occurs when u_id does not refer to a valid user

    Return Value:
        a dictionary {dm_id, dm_name}

    Assumption:
        - a new dm is created everytime a creator creates one even there is already
         a dm with the same creator and dm members
    '''

    data = load_data()
    dms = data['dms']
    dm_id = len(dms) + 1

    if not is_valid_token(token):
        raise AccessError("Token is invalid.")

    user_id = is_valid_token(token)['user_id']
    handles = []

    for id in u_ids:
        if not is_valid_user_id(id):
            raise InputError(f"u_id: {id} is not a valid user.")

        user_handle = find_user(id, data)['account_handle']
        handles.append(user_handle)

    handles.append(find_user(user_id, data)['account_handle'])
    dm_name = ','.join(sorted(handles))

    dm_dict = {
        'creator': user_id,
        'dm_id': dm_id,
        'name': dm_name,
        'members': u_ids,
        'messages': []
    }

    dms.append(dm_dict)
    save_data(data)

    return {'dm_id': dm_id, 'dm_name': dm_name}

