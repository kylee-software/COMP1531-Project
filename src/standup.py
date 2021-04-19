from json import load
from os import access
from src.message import message_send_v2
from src.helper import is_valid_token, is_valid_channel_id, is_user_in_channel, find_channel, load_data, save_data
from src.error import AccessError, InputError
from src.data import dataStore
from datetime import datetime, timezone
import threading

def standup_start_v1(token, channel_id, length):

    #data = dataStore
    data = load_data()

    if not is_valid_token(token):
        raise AccessError('Invalid Token')
    token_data = is_valid_token(token)

    if not is_valid_channel_id(channel_id):
        raise InputError('Invalid channel_id')
    
    if standup_active_v1(token, channel_id)['is_active'] == True:
        raise InputError("Standup already in progress")

    if not is_user_in_channel(channel_id, token_data['user_id'], data):
        raise AccessError("Authorised user is not part of this channel")

    channel = next(channel for channel in data['channels'] if channel_id == channel_id)
    channel['standup']['is_active'] = True
    channel['standup']['time_finish'] = datetime.now().replace(tzinfo=timezone.utc).timestamp() + length
    channel['standup']['messages'] = ''
    channel['standup']['user_id'] = token_data['user_id']

    t = threading.Timer(length, standup_end, args=[token, channel_id, data])
    t.start()

    save_data(data)
    return channel['standup']['time_finish']

def standup_end(*args):
    channel = find_channel(args[1], args[2])
    message = channel['standup']['messages']
    message_send_v2(args[0], args[1], message)
    chnnel['stanadup']['is_active'] = False

def standup_active_v1(token, channel_id):
    data = load_data()
    if not is_valid_token(token):
        raise AccessError ("Invalid Token")
    
    if not is_valid_channel_id(channel_id):
        raise InputError("Invalid channel_id")

    channel = find_channel(channel_id, data)

    if channel['standup']['is_active'] == False:
        return { 'is_active' : channel['standup']['is_active'],
             'time_finish' : None,
            }
    else:
        return { 'is_active' : channel['standup']['is_active'],
                 'time_finish' : channel['standup']['time_finish'],
                }

def standup_send_v1(token, channel_id, message):
    pass
