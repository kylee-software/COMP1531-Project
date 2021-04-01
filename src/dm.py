from werkzeug.exceptions import UnavailableForLegalReasons
from src.error import InputError, AccessError
from src.helper import is_valid_token, save, load

def dm_invite(token, dm_id, user_id):
    if not is_valid_token(token):
        raise AccessError("Invalid Token")
    token = is_valid_token(token)
    data = load()

    dm = next((dm for dm in data['dms'] if dm['dm_id'] == dm_id), False)
    if not dm:
        raise InputError("Invalid dm_id")

    user = next((user for user in data['users'] if user['user_id'] == user_id), False)
    if not user:
        raise InputError("User doesn't exist")

    if next((member for member in dm['members'] if member['user_id'] == user_id), False):
        raise InputError("User is already a part of that dm")
    
    if not next((token_member for token_member in dm['members'] if token_member['user_id'] == token['user_id']), False):
        raise InputError("Authorised user is not a part of this dm")

    dm['members'].append(user)
    save(data)

    return {}