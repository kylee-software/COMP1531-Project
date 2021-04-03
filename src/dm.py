from src.error import AccessError, InputError
from src.helper import is_valid_user_id, load_data, save_data, is_valid_token, find_user


def dm_details(token, dm_id):
    if not is_valid_token(token):
        raise AccessError("Invalid token")
    token = is_valid_token(token)
    
    data = load_data()

    dm_dict = next((dm for dm in data['dm'] if dm['dm_id'] == dm_id), False)
    #dm_dict = list(filter(lambda dm: dm['dm_id'] == dm_id, data['dm']))[0]
    if not dm_dict:
        raise InputError("dm_id is invalid")

    if dm_dict['members'].count(token['user_id']) == 0:
        raise AccessError("User is not in this DM")

    return_dict = {'name' : dm_dict['name'], 'members' : []}
    for member in dm_dict['members']:
        user = next(user for user in data['users'] if user['user_id'] == member['user_id'])
        return_dict['members'].append({'user_id': user['user_id'],
                                     'email': user['email_address'],
                                     'name_first': user['first_name'], 
                                     'name_last': user['last_name'],
                                     'handle_str': user['account_handle'],
                                     })
    return return_dict


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

