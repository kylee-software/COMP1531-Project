from src.error import AccessError, InputError
from src.helper import is_valid_user_id, load_data, is_valid_channel_id, save_data, is_valid_token, find_user

def dm_remove_v1(token, dm_id):
    '''
    Function to delete a dm

    Arguments:
        token (string)       - an authorisation hash of the user
        dm_id (int)          - dm id of the dm the user is deleting

    Exceptions:
        AccessError  - Occurs when the token invalid or when the user is not the dm creator
        InputError   - Occurs when dm_id does not refer to a valid dm

    Return Value:
        {} on successful removal of a dm

    '''
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(description=f"Auth_user_id: {auth_user_id} is invalid")

    found_dm = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            found_dm = True
            if dm['creator'] != auth_user_id:
                raise AccessError(description=f"user is not dm creator")
            del dm 
            break
            
    if found_dm == False:
        raise InputError(description=f"Dm id was invalid")

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

