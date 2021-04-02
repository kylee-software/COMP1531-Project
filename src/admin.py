from src.error import AccessError, InputError
from src.helper import is_valid_user_id 
from src.helper import is_valid_channel_id, load_data, save_data, is_valid_token

OWNER_PERMISSION = 1
MEMBER_PERMISSION = 2

def admin_changepermission_v1(token, u_id, permission_id):
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(descripton=f"Auth_user_id: {auth_user_id} is invalid")

    if is_valid_user_id (u_id) == False:
        raise InputError(description=f"invalid u_id: {u_id}")

    if permission_id != OWNER_PERMISSION and permission_id != MEMBER_PERMISSION:
        raise InputError(description=f"invalid permission_id: {permission_id}")

    for user in data['users']:
        if user['user_id'] == auth_user_id:
            user_permission = user['permission_id']
            break
    
    if user_permission != OWNER_PERMISSION:
        raise AccessError(description=f"authorised user is not an owner ")
    
    for user in data['users']:
        if user['user_id'] == u_id:
            user['permission_id'] = permission_id
            break
    save_data(data)

    return {}