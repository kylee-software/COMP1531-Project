from src import data as data_file  # to add new channel_id and its corresponding data info to the dictionary
from error import InputError  # to handle InputError

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
    if len(name) > 20:
        raise InputError("Channel name is longer than 20 characters.")

    '''
    Get the number of channels already exist to help to create the channel_id,
    i.e, channel_size + 1 = channel_id
    '''
    channel_id = len(data_file.data['channels']) + 1

    # Add the new channel info to the data
    new_channel = data_file.data['channels'][channel_id - 1]
    new_channel['channel_id'] = channel_id
    new_channel['name'] = name
    new_channel['public_status'] = is_public

    # Add owner info to members list
    new_channel['members'][0]['user_id'] = auth_user_id
    new_channel['members'][0]['channel_owner_status'] = True

    '''
    Add messages --> might have to import channel_messages_v1 from channel
    '''
    # channel_info[channel_id]['messages'] = channel_messages_v1(auth_user_id, channel_id, 0)

    return channel_id
