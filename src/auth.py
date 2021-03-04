import re 
from src.error import InputError
from src.data import data  

def auth_login_v1(email, password):

    if re.fullmatch(r'^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email) is None: 
        raise InputError('Please enter a valid email address.') 
    
    for lists in data['users']:
        for user in lists:
            if user['email_address'] == email:
                if user['account_password'] == password:
                    return user['user_id']  
                else:
                    raise InputError('Incorrect Password.') 
            else:
                raise InputError('Email not found.') 

def auth_register_v1(email, password, name_first, name_last):
    
    password_length = len(password)
    first_name_length = len(name_first)
    last_name_length = len(name_last)
    name_join = '' 
    handle = ''  

    if re.fullmatch (r'^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email) is None: 
        return InputError('Please enter a valid email address.')
    else:
        if password_length < 6:
            raise InputError('Password is less than 6 characters.') 
        else:
            if first_name_length < 1 or first_name_length > 50:
                raise InputError('First name is not a valid length.')
            else:
                if last_name_length < 1 or last_name_length > 50:
                    raise InputError('Last name is not a valid length.') 
                else:
                    name_join = name_first + name_last

                    if len(name_join) > 20:
                        for character in name_join[0:20]:
                            handle += character 
                    else:
                        handle = name_join
                    
                    for characters in handle:
                        if characters == '@' or characters == ' ' :
                            raise InputError("No @ or whitespace allowed in handles.")

                    number = 0
                    numbering_start = True 
                    for lists in data['users']:
                        for user in lists:
                            if user['account_handle'] == handle:
                                if numbering_start is True:
                                    handle = handle + str(number)
                                    numbering_start = False 
                                else:
                                    number += 1
                                    handle = handle + str(number)

                    new_user = {
                        'first_name': name_first,
                        'last_name': name_last,
                        'email_address': email,
                        'account_password': password,
                        'global_owner_status': False,
                        'account_handle': handle,
                        'user_id': len(data['users']) + 1,  
                    } 

                    data['users'].append(new_user)
