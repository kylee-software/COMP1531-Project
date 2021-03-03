from data import channel_info  # to add new channel_id and its corresponding data info to the dictionary
from src.error import InputError # to handle InputError

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
    channel_id = len(channel_info) + 1

    # Add the new channel info to the data
    channel_info[channel_id]['channel_id'] = channel_id
    channel_info[channel_id]['name'] = name
    channel_info[channel_id]['public_status'] = is_public

    # Add owner info to members list
    channel_info[channel_id]['members'][0]['user_id'] = auth_user_id
    channel_info[channel_id]['members'][0]['channel_owner_status'] = True

    '''
    Add messages --> might have to import channel_messages_v1 from channel
    '''
    # channel_info[channel_id]['messages'] = channel_messages_v1(auth_user_id, channel_id, 0)

    return {'channel_id': channel_id}
