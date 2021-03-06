from src.data import data
from src.error import InputError, AccessError

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    """Returns a list of all channels

    Args:
        auth_user_id (int): a valid user_id

    Raises:
        AccessError: occurs when auth_user_id is invalid

    Returns:
        Dictionary: key 'channels' and list of dicts with keys channel_id and name
    """
    foundID = False
    for user in data['users']:
        if user.get('user_id') == auth_user_id:
            foundID = True
    if foundID == False: 
        raise AccessError
    
    returnDict = {'channels': []}
    for channel in data['channels']:
        newChannel = {'channel_id': channel.get('channel_id'),
                        'name': channel.get('name')}
        returnDict['channels'].append(newChannel)

    return returnDict

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
