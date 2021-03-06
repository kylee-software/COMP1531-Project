import hashlib
from types import prepare_class
import jwt
import json
from src.data import dataStore

SECRET = 'WED09B-ECHO'

def load_data():
    '''
    loads the data from a json file called data.json

    Return Type:
        data that was stored in data.json if its in the 
        correct format ({'users':[], 'channels':[]})

        or returns empty data ({'users':[], 'channels':[]}) 
        if the data in the json file was the incorrect format
    '''
    global dataStore
    try:
        with open('src/data.json', 'r') as FILE:
            data = json.load(FILE)
            if 'users' and 'channels' and 'dms' and 'msg_counter' in data:
                #return data
                dataStore['users'] = data['users']
                dataStore['channels'] = data['channels']
                dataStore['dms'] = data['dms']
                dataStore['msg_counter'] = data['msg_counter']
                dataStore['dreams_stats'] = data['dreams_stats']
                return
            else:
                #return {'users': [], 'channels': [], 'dms': [], 'msg_counter': 0}
                dataStore['users'] = []
                dataStore['channels'] = []
                dataStore['dms'] = []
                dataStore['msg_counter'] = 0
                dataStore['dreams_stats'] = {'channels_exist':[], 
                                        'dms_exist':[], 
                                        'messages_exist':[], 
                                        'utilization_rate':0}
                        
                return
                
    except:
        """print('THE DATA IS BEING RESEEEEEEEET')
        with open('src/data.json', 'w') as FILE:
            data_setup = {'users': [], 
                        'channels': [], 
                        'dms': [], 
                        'msg_counter': 0,
                        'dreams_stats': {'channels_exist':[], 
                                        'dms_exist':[], 
                                        'messages_exist':[], 
                                        'utilization_rate':0}
                        }
            json.dump(data_setup, FILE)
            return data_setup"""
        dataStore['users'] = []
        dataStore['channels'] = []
        dataStore['dms'] = []
        dataStore['msg_counter'] = 0
        dataStore['dreams_stats'] = {'channels_exist':[], 
                                        'dms_exist':[], 
                                        'messages_exist':[], 
                                        'utilization_rate':0}

def return_valid_tagged_handles(message, channel_id):
    data = dataStore
    split_message = message.split()
    handles = []
    for word in split_message:
        if word.startswith('@'):
            handles.append(word.strip('@'))

    real_handles = []
    for handle in handles:
        if next((user for user in data['users'] if user['account_handle'] == handle), False):
            real_handles.append(handle)

    real_handles_in_channel = []
    channel = next(
        (channel for channel in data['channels'] if channel['channel_id'] == channel_id), False)
    for handle in real_handles:
        for member in channel['members']:
            m_handle = next(user['account_handle']
                            for user in data['users'] if user['user_id'] == member['user_id'])
            if m_handle == handle:
                real_handles_in_channel.append(handle)

    return real_handles_in_channel


def is_valid_user_id(auth_user_id):
    '''
    checks the given auth_user_id is valid

    Arguments:
        auth_user_id (int)      - user_id that needs checking

    Return Value:
        Returns True is user id is valid, False if it is not
    '''

    data = dataStore
    for user in data['users']:
        if user['user_id'] == auth_user_id:
            return True
    return False


def is_valid_channel_id(channel_id):
    '''
    checks the given channel_id is valid

    Note:
        requires implementation of channels_create_v1 before testing

    Arguments:
        channel_id (int)      - channel_id that needs checking

    Return Value:
        Returns True is channel_id is valid, False if it is not
    '''

    data = dataStore
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False


def is_valid_dm_id(dm_id):
    data = dataStore
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            return True
    return False


def hash_password(password):
    '''
    hashes a given string 

    Arguments:
        password (string)      - password to hash

    Return Value:
        Returns hashed password
    '''
    return hashlib.sha256(password.encode()).hexdigest()


def create_token(user_id, session_id):
    '''
    creates a token with a given user id and session id

    Arguments:
        user_id
        session_id

    Return Value:
        Returns jwt token
    '''
    return jwt.encode({'user_id': user_id, 'session_id': session_id}, SECRET, algorithm='HS256')


def is_valid_token(token):
    '''
    checks if a token has been tampered with

    Arguments:
        token

    Return Value:
        Returns False if the token is invalid, returns the payload if the token is valid
    '''
    data = dataStore
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    except:
        jwt.exceptions.InvalidSignatureError()
        return False
    else:
        user = next(
            (user for user in data['users'] if user['user_id'] == payload['user_id']), False)
        if user:
            if user['session_list'].count(payload['session_id']) != 0:
                return payload
        return False


def save_data(data):
    '''
    saves the input data to a json file called data.json

    Arguments:
        data       - data to save

    Exceptions:
        If data to be saved is not of the format 
            {'users':[], 'channels':[]} an exception is raised
    '''

    if 'users' and 'channels' and 'dms' and 'msg_counter' in data:
        with open('src/data.json', 'w') as FILE:
            json.dump(data, FILE)
    else:
        raise Exception(
        )


def find_user(user_id, data):
    for user in data['users']:
        if user['user_id'] == user_id:
            return user


def find_channel(channel_id, data):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel


def find_dm(dm_id, data):
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            return dm


def is_user_in_channel(channel_id, user_id, data):
    channel = find_channel(channel_id, data)
    for member in channel['members']:
        if member['user_id'] == user_id:
            return True
    return False


def invite_notification_message(token, id, name, is_channel):
    data = dataStore

    if is_channel:
        token_user = find_user(token['user_id'], data)
        return {"channel_id": id, "dm_id": -1, "notification_message": f"{token_user['account_handle']} added you to {name}"}
    else:
        token_user = find_user(token['user_id'], data)
        return {"channel_id": -1, "dm_id": id, "notification_message": f"{token_user['account_handle']} added you to {name}"}


def message_notification_message(token, id, name, is_channel, message):
    data = dataStore
    if is_channel:
        token_user = find_user(token['user_id'], data)
        notification_message = f"{token_user['account_handle']} tagged you in {name}: {message[:20]}"
        return {'channel_id': id, 'dm_id': -1, 'notification_message': notification_message}
    else:
        token_user = find_user(token['user_id'], data)
        notification_message = f"{token_user['account_handle']} tagged you in {name}: {message[:20]}"
        return {'channel_id': -1, 'dm_id': id, 'notification_message': notification_message}


def find_user_channel_owner_status(channel_id, user_id, data):
    channel = find_channel(channel_id, data)
    for member in channel['members']:
        if member['user_id'] == user_id:
            return member['permission_id']


def is_user_in_dm(dm_id, user_id, data):
    dm = find_dm(dm_id, data)
    for member in dm['members']:
        if member == user_id:
            return True
    if dm['creator'] == user_id:
        return True
    return False


def find_message_source(message_id, data):
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return channel

    for dm in data['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                return dm
    return None


def find_message(message_id, data):
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return message['message']

    for dm in data['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                return message['message']
    return ""


def tag_users(message, sender_handle, dm_id, channel_id):
    data = dataStore
    split_message = message.split()
    tagged_handles = []
    for word in split_message:
        if word.startswith('@'):
            tagged_handles.append(word.strip('@'))

    users_tagged = []
    for handle in tagged_handles:
        for user in data['users']:
            if handle == user['account_handle']:
                users_tagged.append(user)

    if dm_id != -1:
        if is_valid_dm_id(dm_id) == True:
            dm = find_dm(dm_id, data)
            for user in users_tagged:
                if user['user_id'] in dm['members']:
                    notification_message = f"{sender_handle} tagged you in {dm['name']}: {message[:20]}"
                    return user['user_id'], {'channel_id': -1, 'dm_id': dm_id, 'notification_message': notification_message}

    return False
