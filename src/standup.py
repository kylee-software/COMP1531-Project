from json import load
from os import access
from src.message import message_send_v2
from src.helper import is_valid_token, is_valid_channel_id, is_user_in_channel, find_channel, save_data
from src.error import AccessError, InputError
from src.data import dataStore
from datetime import datetime, timezone
import threading

def standup_start_v1(token, channel_id, length):
    """starts a standup with the duration length in the channel referenced by channel_id

    Args:
        token (str): a jwt encoded string which decodes to a dict with values 'user_id' and 'session_id'
        channel_id (int): int referencing the channel the standup will take place in
        length (int): duration in seconds the standup will last

    Raises:
        AccessError: raised when token is invalid
        InputError: raised when the channel_id is invalid
        InputError: raised when a standup is already in progress
        AccessError: raised when the user referenced by token is not in the channel

    Returns:
        dict: a dictionary with key 'time_finish' and value being a unix timestamp
    """
    #data = dataStore
    data = dataStore

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

    global t
    t = threading.Timer(length, standup_end, args=[token, channel_id, data])
    t.start()

    save_data(data)
    return {'time_finish': channel['standup']['time_finish']}

def standup_end(*args):

    channel = find_channel(args[1], args[2])
    
    message = channel['standup']['messages']
    message_send_v2(args[0], args[1], message)
    
    data = dataStore
    channel = next(channel for channel in data['channels'] if channel['channel_id'] == args[1])
    channel['standup']['is_active'] = False
    channel['standup']['time_finish'] = None
    save_data(data)
    
    global t
    t.cancel()

def standup_active_v1(token, channel_id):
    """Tells if a standup is currently active in the channel referenced by channel_id

    Args:
        token (str): jwt encoded string of dict with keys 'user_id' and 'session_id'
        channel_id (id): id of the channel being checked

    Raises:
        AccessError: raised when token is invalid
        InputError: raised when channel_id is invalid

    Returns:
        dict:  dictionary with keys 'is_active', boolean, and 'time_finish', a unix timestamp
    """
    try:
        channel_id = int(channel_id)
    except Exception as e:
        raise InputError(description='channel_id must be an integer') from e

    data = dataStore
    if not is_valid_token(token):
        raise AccessError ("Invalid Token")
    
    if not is_valid_channel_id(channel_id):
        raise InputError("Invalid channel_id")

    channel = find_channel(channel_id, data)

    if channel['standup']['is_active'] == False:
        return { 'is_active' : False,
             'time_finish' : None,
            }
    else:
        return { 'is_active' : True,
                 'time_finish' : channel['standup']['time_finish'],
                }

def standup_send_v1(token, channel_id, message):
    """send a message to a standup

    Args:
        token (str): jwt encoded string with keys 'user_id' and 'session_id'
        channel_id (int): id of the channel the message is being sent to 
        message (str): the message being sent

    Raises:
        AccessError: raised when token is invalid
        InputError: raised when channel_id is invalid
        InputError: raised when the message being sent is over 1000 characters
        InputError: raised when there is no active standup
        AccessError: raised when the user referenced by token is not in the chnnel
    """
    data = dataStore
    if not is_valid_token(token):
        raise AccessError("Invalid token")
    token_data = is_valid_token(token)

    if not is_valid_channel_id(channel_id):
        raise InputError('Invalid channel_id')

    if len(message) > 1000:
        raise InputError("Message is longer than 1000 characters")

    if not standup_active_v1(token, channel_id)['is_active']:
        raise InputError("No active standup")

    if not is_user_in_channel(channel_id, token_data['user_id'], data):
        raise AccessError("User is not in channel")

    channel = find_channel(channel_id, data)
    channel['standup']['messages'] = channel['standup']['messages'] + ' ' + message   

    save_data(data)

    return {}