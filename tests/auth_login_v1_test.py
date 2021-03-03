import pytest
# import auth function and clear function 
#run clear then the test 
# login clear so always running on empty so always invalid 

# Test exception - Email given is not valid (wrong format)
def test_invalid_email(): 
    invalid_email = '@unsw.edu.au'
    with pytest.raises(InputError): 
        auth_login_v1(invalid_email, 'password')

# Test exception - Email given does not match a user's email (email doesn't exist)
def test_given_email_nonexistent():
    auth_register 
    with pytest.raises(InputError):
            auth_login()
    
    auth register
    with pytest.raises
    auth_login()
# Test exception - password given is not correct  
def test_password_incorrect():
    auth_register_v1('testing@unsw.edu.au, 'password', 'first', 'last')
    with pytest.raises(InputError):
        auth_
# Test where auth_user_id given as email and password given are correct
def correct_login_details_given(): 
    with pytest.raises(InputError):
     
