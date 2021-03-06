import re 
from src.error import InputError
from src.data import data  

def auth_login_v1(email, password):

    if re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email) == None: 
        raise InputError('Please enter a valid email address.') 
    
    for user in data['users']:
        if user['email_address'] == email:
            if user['account_password'] == password:
                return {'auth_user_id':user['user_id']}    
            else:
                raise InputError('Incorrect Password.') 
    raise InputError('Email not found.') 

def auth_register_v1(email, password, name_first, name_last):
    global data 
    password_length = len(password)
    first_name_length = len(name_first)
    last_name_length = len(name_last)

    if re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email) is None: 
        raise InputError('Please enter a valid email address.')
 
    for user in data['users']: 
            if user['email_address'] == email:
                raise InputError('Email already registered.') 

    if password_length < 6:
            raise InputError('Password is less than 6 characters.')    

    if first_name_length < 1 or first_name_length > 50:
        raise InputError('First name is not a valid length.')

    if last_name_length < 1 or last_name_length > 50:
        raise InputError('Last name is not a valid length.') 
                
    handle = name_first + name_last

    if len(handle) > 20:
        handle = handle[0:20] 
    
    for character in handle:
        if character == '@' or character.isspace() : 
            raise InputError("No @ or whitespace allowed in handles.")

    user_list = data['users']
    i = 0
    number = 0
    updated_handle = handle 
    while i < len(user_list):
        user = user_list[i] 
        if user['account_handle'] == updated_handle:
            updated_handle = handle + str (number)
            i = 0
            number += 1
        i += 1
    global_owner_status = False
    if len(data['users']) == 0:
        global_owner_status = True
    new_user = {
        'first_name': name_first,
        'last_name': name_last,
        'email_address': email,
        'account_password': password,
        'global_owner_status': global_owner_status,
        'account_handle': updated_handle,
        'user_id': len(data['users']) + 1,  
    } 

    user_list.append(new_user)

    return {'auth_user_id':new_user['user_id']}
