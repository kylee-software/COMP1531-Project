from src.error import AccessError, InputError
from src.helper import is_valid_user_id, find_user, find_channel
from src.helper import is_valid_channel_id, load_data, save_data, is_valid_token

def message_send_v1(auth_user_id, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }

def message_senddm_v1(token, dm_id, message):
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(descripton=f"Auth_user_id: {auth_user_id} is invalid")

    if len(message) > 1000:
        raise InputError(description=f"message is too long")

    found_dm = False
    found_user = False
    message_id = len(data['messages']) + 1

    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            found_dm = True
        for member in dm['members']:
            if member == auth_user_id:
                found_user = True
            dm['messages'].insert(0, (message, message_id))
    
    if found_dm == False:
        raise InputError(description=f"invalid dm id")

    if found_user == False:
        raise AccessError(description=f"user not in dm")
        
    save_data(data)
    return {message_id}