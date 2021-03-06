from src.error import AccessError, InputError  
from src.helper import is_valid_token, save_data
from src.data import dataStore
from src.helper import is_valid_token, load_data, save_data, find_user
from datetime import datetime

def channels_list_v2(token):
    """Returns a list of channels that the authorised user is a part of

    Args:
        token (string): a valid token, decodes into dict with fiels user_id and session_id

    Raises:
        AccessError: occurs when token is invalid

    Returns:
        Dictionary: has key 'channels' and list of dicts with keys channel_id and name
    """
    data = dataStore
    if not is_valid_token(token):
        raise AccessError(f"Auth_user_id: {token} is invalid")
    token = is_valid_token(token)

    returnDict = {'channels': []}
    for channel in data['channels']:
        if next((member for member in channel['members'] if member['user_id'] == token['user_id']), False):
            newDict = {'channel_id': channel.get('channel_id'),
                            'name': channel.get('name')}
            returnDict['channels'].append(newDict)
        
    return returnDict

def channels_listall_v2(token):
    """Returns a list of all channels

    Args:
        token (str): jwt encode dict with keys 'session_id' and 'auth_user_id'

    Raises:
        AccessError: occurs when token is invalid

    Returns:
        Dictionary: key 'channels' and list of dicts with keys channel_id and name
    """
    data = dataStore
    if not is_valid_token(token):
        raise AccessError(f"Auth_user_id: {token} is invalid")
    token = is_valid_token(token)

    returnDict = {'channels': []}
    for channel in data['channels']:
        newChannel = {'channel_id': channel.get('channel_id'),
                      'name': channel.get('name')}
        returnDict['channels'].append(newChannel)

    return returnDict


def channels_create_v2(token, name, is_public):
    '''
    Function to create a channel that is either a public or private with a given name

    Arguments:
        token (string)       - an authorisation hash of the user
        name (string)        - name for the channel
        is_public (boolean)  - True if the channel is public, False if it's private

    Exceptions:
        AccessError  - Occurs when the token invalid
        InputError   - Occurs when channel name is greater than 20 characters or no name is entered

    Return Value:
        a dictionary {channel_id}
    '''

    if not is_valid_token(token):
        raise AccessError("Token is invalid")

    if len(name) > 20 or len(name) == 0:
        raise InputError("No channel name is entered or channel name is longer than 20 characters.")

    data = dataStore
    channels = data['channels']
    user_id = is_valid_token(token)['user_id']

    '''
        Get the number of channels already exist to help to create the channel_id,
        i.e, channel_id = channel_size + 1
    '''
    channel_id = len(channels) + 1

    # Add the new channel info to the data
    new_channel = {'channel_id': channel_id,
                   'name': name,
                   'owner': [user_id],
                   'members': [
                       {'user_id': user_id,  # add the owner to the members list
                        'permission_id': 1}  # owner has permission_id = 1
                   ],
                   'public_status': is_public,
                   'messages': [],
                   'standup': {'is_active': False,
                                'time_finish': None,
                                'messages' : '',
                                'user_id': None,
                            },
                   }
    channels.append(new_channel)
    
    user = find_user(user_id, data)
    channels_joined = len(user['user_stats']['channels_joined']) + 1
    user['user_stats']['channels_joined'].append({'num_channels_joined':channels_joined, 'time_stamp':int(datetime.now().timestamp())})
    
    if len(data['dreams_stats']['channels_exist']) == 0:
        channels_exist = 1
    else:
        channels_exist = data['dreams_stats']['channels_exist'][-1]['num_channels_exist'] + 1

    data['dreams_stats']['channels_exist'].append({'num_channels_exist':channels_exist, 'time_stamp':int(datetime.now().timestamp())})
    
    save_data(data)
    return {'channel_id': channel_id}
