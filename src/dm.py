from werkzeug.exceptions import UnavailableForLegalReasons
from src.error import InputError, AccessError
from src.helper import is_valid_token, save_data, load_data, is_valid_user_id

def dm_invite(token, dm_id, user_id):
    if not is_valid_token(token):
        raise AccessError("Invalid Token")
    token = is_valid_token(token)
    data = load_data()

    dm = next((dm for dm in data['dms'] if dm['dm_id'] == dm_id), False)
    if not dm:
        raise InputError("Invalid dm_id")

    if not is_valid_user_id(user_id):
        raise InputError("User doesn't exist")

    if dm['members'].count(user_id) != 0:
        raise InputError("User is already a part of that dm")
    
    if dm['members'].count(token['user_id']) == 0:
        raise InputError("Authorised user is not a part of this dm")

    dm['members'].append(user_id)
    save_data(data)

    return {}