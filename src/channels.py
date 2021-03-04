from src.data import data
from src.error import AccessError

def channels_list_v1(auth_user_id):
    validId = False
    for user in data['users']:
        if user['user_id'] == auth_user_id:
            validId = True
    if validId == False:
        raise AccessError

    returnList = []
    for channel in data['channels']:
        for members in channel['members']:
            for member in members:
                if member['user_id'] == auth_user_id:
                    returnList.append(channel)

    return returnList

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
