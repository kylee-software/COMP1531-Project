from src.data import data
from src.helper import check_auth_user_id_v1

def channels_list_v1(auth_user_id):
    """Returns a list of channels that the given auth_user_id is a part of

    Args:
        auth_user_id ([int]): [a valide user_id]

    Raises:
        AccessError: [occurs when auth_user_id is invalid]

    Returns:
        Dictionary: key 'channels' and list of dicts with keys channel_id and name
    """
    check_auth_user_id_v1(auth_user_id)

    returnDict = {'channels': []}
    for channel in data['channels']:
        for member in channel['members']:
            if member['user_id'] == auth_user_id:
                newDict = {'channel_id': channel.get('channel_id'),
                            'name': channel.get('name')}
                returnDict['channels'].append(newDict)

    return returnDict

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
