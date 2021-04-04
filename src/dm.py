from error import AccessError, InputError
from helper import is_valid_user_id, load_data, save_data, is_valid_token, find_user

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

def dm_messages_v1(token, dm_id, start):
    '''
    Function to return up to 50 messages between "start" and "start + 50"

    Arguments:
        token (string)      - an authorisation hash of the user
        dm_id (int)         - dm_id of the dm the user is part of
        start (int)         - show messages starting from start; start = 0 means the most recent message

    Exceptions:
        AccessError - Occurs when the token is invalid and authorised user is not a member of the dm

        InputError  - Occurs when dm_id is invalid and "start" is greater than\
        the total number of messages in the dm

    Return Value:
        Returns {messages, start, end} where messages is a dictionary
    '''

    data = load_data()

    if not is_valid_token(token):
        raise AccessError("Token is invalid")

    user_id = is_valid_token(token)['user_id']
    dms = data['dms']
    is_member = False
    is_valid_dm_id = False
    dm_messages = []

    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            is_valid_dm_id = True
            dm_dict = dm
            for member in dm['members']:
                if member == user_id:
                    is_member = True
            dm_messages = dm['messages']

    if not is_valid_dm_id:
        raise InputError("Invalid DM id!")

    if not is_member:
        raise AccessError("User not part of the dm!")

    # Check valid start number
    if start >= len(dm_messages):
        raise InputError("Start is greater than the total number of messages in the dm.")

    # calculate the ending return value
    end = start + 50 if (start + 50 < len(dms) - 1) else -1
    messages_dict = {'messages': []}

    if end == -1:
        for i in range(start, len(dm_messages)):
            messages_dict['messages'].append(dm_messages[i])
    else:
        for i in range(start, end):
            messages_dict['messages'].append(dm_messages[i])

    messages_dict['start'] = start
    messages_dict['end'] = end

    return messages_dict
