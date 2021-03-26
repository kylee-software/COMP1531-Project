import hashlib
import jwt
import json

SECRET = 'WED09B-ECHO'

def is_valid_user_id(auth_user_id):
    '''
    checks the given auth_user_id is valid

    Arguments:
        auth_user_id (int)      - user_id that needs checking

    Return Value:
        Returns True is user id is valid, False if it is not
    '''

    data = load_data()
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

    data = load_data()
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
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
    return jwt.encode({'user_id':user_id,'session_id': session_id}, SECRET, algorithm='HS256')

def is_valid_token(token):
    '''
    checks if a token has been tampered with

    Arguments:
        token

    Return Value:
        Returns False if the token is invalid, returns the payload if the token is valid
    '''
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    except:
        jwt.exceptions.InvalidSignatureError()
        return False
    else:
        return payload

def save_data(data):
    '''
    saves the input data to a json file called data.json

    Arguments:
        data       - data to save
    '''
    with open('src/data.json', 'w') as FILE:
        json.dump(data, FILE)

def load_data():
    '''
    loads the data from a json file called data.json

    Return Type:
        data that was stored in data.json
    '''
    with open('src/data.json','r') as FILE:
        return json.load(FILE)


#def find_user(user_id, data):
 #   for user in data['users']:
 #       if user['user_id'] == user_id:
 #           return user
