from src.error import AccessError, InputError  
from src.helper import is_valid_token, is_valid_user_id, load_data, save_data

def channels_list_v1(token):
    """Returns a list of channels that the given auth_user_id is a part of

    Args:
        token (string): a valid token, decodes into dict with fiels user_id ans session_id

    Raises:
        AccessError: occurs when token is invalid

    Returns:
        Dictionary: has key 'channels' and list of dicts with keys channel_id and name
    """
    data = load_data()
    if not is_valid_user_id(token):
        raise AccessError(f"Auth_user_id: {token} is invalid")
    token = is_valid_token(token)

    returnDict = {'channels': []}
    for channel in data['channels']:
        if next((member for member in channel['members'] if member['user_id'] == token['user_id']), False):
            newDict = {'channel_id': channel.get('channel_id'),
                            'name': channel.get('name')}
            returnDict['channels'].append(newDict)
        
    return returnDict

def channels_listall_v1(auth_user_id):
    """Returns a list of all channels

    Args:
        auth_user_id (int): a valid user_id

    Raises:
        AccessError: occurs when auth_user_id is invalid

    Returns:
        Dictionary: key 'channels' and list of dicts with keys channel_id and name
    """
    data = load_data()
    if is_valid_user_id(auth_user_id) == False:
        raise AccessError(f"Auth_user_id: {auth_user_id} is invalid")
    
    returnDict = {'channels': []}
    for channel in data['channels']:
        newChannel = {'channel_id': channel.get('channel_id'),
                        'name': channel.get('name')}
        returnDict['channels'].append(newChannel)

    return returnDict

def channels_create_v1(auth_user_id, name, is_public):
    '''
     Function to create a channel that is either a public or private channel with a given name

    Arguments:
        auth_user_id (int)      - user_id of the person already in the channel
        name (string)           - name for the channel
        is_public (boolean)     - True if the channel is public, False if it's private

    Exceptions:
        AccessError - Occurs when the given auth_user_id is an unauthorised user
        InputError  - Occurs when channel name is greater than 20 characters

    Return Value:
        Returns {channel_id} upon valid channel name
    '''
    data = load_data()

    if is_valid_user_id(auth_user_id) == False:
        raise AccessError(f"Auth_user_id: {auth_user_id} is invalid")

    if len(name) > 20:
        raise InputError("Channel name is longer than 20 characters.")

    # locate channels in the data_dict dict
    channels = data['channels']

    '''
        Get the number of channels already exist to help to create the channel_id,
        i.e, channel_size + 1 = channel_id
        '''
    channel_id = len(channels) + 1

    # Add the new channel info to the data
    new_channel = {'channel_id': channel_id,
                   'name': name,
                   'public_status': is_public}
    channels.append(new_channel)

    # Add owner info to members list
    new_channel['members'] = [{'user_id': auth_user_id,
                               'permission_id': 1}]

    save_data(data)
    return {'channel_id': channel_id}
