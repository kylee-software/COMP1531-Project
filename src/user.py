from src.helper import is_valid_token, load_data, is_valid_user_id, find_user, save_data
from src.error import AccessError, InputError


def user_profile_v2(token, u_id):
    """Given a valid u_id returns details about the user 

    Args:
        token (str): a jwt encoded dict with keys session_id and user_id
        u_id (int): the users id that the token wants details about

    Raises:
        AccessError: raises if token is invalid
        InputError: raises if user_id is invalid

    Returns:
        {user}: a dictionary with values u_id, email, name_first, name_last and handle_str
    """
    if not is_valid_token(token):
        raise AccessError("Invalid token")
    if not is_valid_user_id(u_id):
        raise InputError("Invalid user_id")

    data = load_data()
    token = is_valid_token(token)
    user = next(user for user in data['users'] if user['user_id'] == u_id)

    return {'user' : {  'u_id' : u_id,
                        'email' : user['email_address'],
                        'name_first' : user['first_name'],
                        'name_last' : user['last_name'],
                        'handle_str' : user['account_handle'],                            
                     }
            }

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(token, handle_str):
    data = load_data()
    token_data = is_valid_token(token)

    if token_data == False:
        raise AccessError(description=f"Token invalid")
    
    auth_user_id = token_data['user_id']
    if is_valid_user_id (auth_user_id) == False:
        raise AccessError(description=f"Auth_user_id: {auth_user_id} is invalid")

    if len(handle_str) <= 3 or len(handle_str) >= 20:
        raise InputError(description=f"handle string is incorrect length, must be between 3 and 20 characters")

    for user in data['users']:
        if user['account_handle'] == handle_str:
            raise InputError(description=f"handle string is already taken")
            
    user = find_user(auth_user_id, data)
    user['account_handle'] = handle_str

    save_data(data)
    return {
    }