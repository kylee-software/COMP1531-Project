from src.helper import is_valid_token, load
from src.error import AccessError, InputError


def dm_details(token, dm_id):
    if not is_valid_token(token):
        raise AccessError("Invalid token")
    token_payload = is_valid_token(token)
    
    data = load()

    dm_dict = next((dm for dm in data['dm'] if dm['dm_id'] == dm_id), False)
    #dm_dict = list(filter(lambda dm: dm['dm_id'] == dm_id, data['dm']))[0]
    if not dm_dict:
        raise InputError("dm_id is invalid")

    if dm_dict['members'].count(token_payload['user_id']) == 0:
        raise AccessError("User is not in this DM")
    
    return {'name': dm_dict['name'], 'members' : dm_dict['members']}
