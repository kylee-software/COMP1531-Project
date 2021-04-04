
from src.helper import load_data, save_data, is_valid_token
from src.error import AccessError

def clear_v1():
    """empties the data dictionary
    """
    save_data({'users':[], 'channels':[], 'dms':[], 'msg_counter':0})

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

def notifications_get_v1(token):
    if not is_valid_token(token):
        raise AccessError("Invalid Token")
    token = is_valid_token(token)
    data = load_data()
    user = next(user for user in data['users'] if user['user_id'] == token['user_id'])
    return {'notifications': user['notifications'][:20]}