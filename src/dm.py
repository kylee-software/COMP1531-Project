from src.error import AccessError, InputError
from src.helper import is_valid_user_id 
from src.helper import is_valid_channel_id, load_data, save_data

def dm_remove(token, dm_id):
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(descripton=f"Auth_user_id: {auth_user_id} is invalid")

    found_dm = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            found_dm = True
            if dm['dm_creator'] != auth_user_id:
                raise AccessError(description=f"user is not dm creator")
            del dm 
            break
            
    if found_dm = False:
        raise InputError(description=f"Dm id was invalid")

    return {}