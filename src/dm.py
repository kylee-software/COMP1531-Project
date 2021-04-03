from src.error import AccessError, InputError
from src.helper import is_valid_token, load_data, is_valid_user_id, save_data, find_user


def dm_list_v1(token):
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError("Invalid Token.")

    data = load_data()
    dm_list = []

    for dm in data['dms']:
        for member in dm['members']:
            if member == decoded_token['user_id']:
                dm_list.append(dm['dm_id'])
                break

    return {'dms': dm_list}


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


def dm_leave_v1(token, dm_id):
    decoded_token = is_valid_token(token)
    if decoded_token is False:
        raise AccessError("Invalid Token.")

    data = load_data()

    dm_id_found = False
    user_in_dm = False

    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm_id_found = True
            for member in dm['members']:
                if member == decoded_token['user_id']:
                    user_in_dm = True
            break

    if dm_id_found is False:
        raise InputError('Valid DM not found.')

    if user_in_dm is False:
        raise AccessError('User is not a member of this DM.')

    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm['members'].remove(decoded_token['user_id'])

    save_data(data)

    return {}
