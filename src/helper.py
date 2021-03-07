from src.data import data
from src.error import AccessError

def check_auth_user_id_v1(auth_user_id):
    global data
    for user in data['users']:
        if user['user_id'] == auth_user_id:
            return 
    raise AccessError(f"Auth_user_id: {auth_user_id} is invalid")
    
