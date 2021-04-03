from src.error import AccessError
from src.helper import is_valid_token, load_data


def dm_create_v1(token, u_ids):
    pass


def dm_list_v1(token):

    if is_valid_token(token) is False:
        return AccessError("Invalid Token.")

    dm_list = []
    user_ids = is_valid_token(token)
    data = load_data()

    for dms in data:
        for dm in dms:
            for member in dm['members']:
                if member == user_ids['user_id']:
                    dm_list.append(dm['dm_id'])
                    break

    return {'dms': dm_list}
