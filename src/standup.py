from json import load
from os import access
from src.message import message_send_v2
from src.helper import is_valid_token, is_valid_channel_id, is_user_in_channel, find_channel, load_data, save_data
from src.error import AccessError, InputError
from src.data import dataStore
from datetime import datetime, timezone
import threading

def standup_start_v1(token, channel_id, length):

   

def standup_active_v1(token, channel_id):
    data = load_data()
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
    pass
