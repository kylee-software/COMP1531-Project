from src.helper import load_data, save_data

def clear_v1():
    """empties the data dictionary
    """
    save_data({'users':[], 'channels':[]})

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
