from src.data import data as data_dict  # to add new channel_id and its corresponding data info to the dictionary
from src.error import InputError, AccessError  # to handle InputError

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
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    '''
     Function to create a channel that is either a public or private channel with a given name

    Arguments:
        auth_user_id (int)      - user_id of the person already in the channel
        name (string)           - name for the channel
        is_public (boolean)         - True if the channel is public, False if it's private

    Exceptions:
        AccessError - Occurs when the given auth_user_id is an unauthorised user
        InputError  - Occurs when channel name is greater than 20 characters

    Return Value:
        Returns {channel_id} upon valid channel name
    '''

    if auth_user_id['auth_user_id'] >= len(data_dict['users']):
        raise AccessError("Unauthorised user")

    if len(name) > 20:
        raise InputError("Channel name is longer than 20 characters.")

    # locate channels in the data dict
    channels = data_dict['channels']

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

    return {'channel_id': channel_id}
