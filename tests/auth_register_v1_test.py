import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.other import clear_v1 
from src.error import InputError 

# Test exception - Email entered is not valid (wrong format)
def test_given_email_is_invalid():
    clear_v1() 

    with pytest.raises(InputError):
        auth_register_v1('@unsw.edu.au', 'password', 'first1', 'last1')
    
    with pytest.raises(InputError):
        auth_register_v1('test.unsw.edu.au', 'password', 'first2', 'last2')

    with pytest.raises(InputError):
        auth_register_v1('test@.au', 'password', 'first3', 'last3')
    
    with pytest.raises(InputError):
        auth_register_v1('test_special!!!@unsw.edu.au', 'password', 'firstspecial', 'lastspecial')

# Test exception - Email entered already exists (belongs to an existing user)
def test_email_already_exists():
    clear_v1()

    auth_register_v1('testing123@unsw.au', 'password', 'first123', 'last123')
    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.au', 'hello123', 'first1', 'last1')
    
    auth_register_v1('testing567@unsw.au', 'password', 'first567', 'last567')
    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.au', 'hello567', 'first2', 'last2')
    
    auth_register_v1('testing890@unsw.au', 'password', 'first890', 'last890')
    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.au', 'hello890', 'first3', 'last3')

# Test exception - Password given is less than 6 Characters
def test_password_incorrect_length():
    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.au', '', 'first1', 'last1')  

    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.au', '2', 'first2', 'last2') 
    
    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.au', '@3456', 'first3', 'last3') 

# Test exception - First name given is between 1 and 50 inclusive 
def test_first_name_valid_length():
    clear_v1() 

    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.au', 'password', '', 'last1') 
    
    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.au', 'password', 'thisfirstnameismorethanfiftycharacterslong123123123123123', 'last2')
    
    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.au', 'password', 'thisfirstnamecontainsspecialcharacters##^^&&**!!123123123', 'last3')   

# Test exception - Last name given is between 1 and 50 inclusive 
def test_last_name_valid_length():
    clear_v1()
    
    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.au', 'password', 'first1', '')
    
    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.au', 'password', 'first2', 'thislastnameismorethanfiftycharacterslong123123123123123') 
    
    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.au', 'password', 'first3', 'thislastnamecontainsspecialcharacters##^^&&**!!123123123')

# Test - if handle generated has whitespace it raises an error as not allowed 
def test_no_whitespace():
    clear_v1() 

    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.au', 'password', 'first name', 'last name')
    
    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.au', 'password', '   first', 'last') 

    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.au', 'password', 'first', 'last   ')

# Test - if handle generated has @ it raises an error as not allowed
def test_no_at_symbol():
    clear_v1()

    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.au', 'password', 'firstn@me', 'l@stn@me') 
    
    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.au', 'password', '@first', 'last')

    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.au', 'password', 'first', 'last@')

# Test - if handle generated contains both @ and whitespace it raises an error as not allowed 
def test_no_at_and_whitespace():
    clear_v1() 

    with pytest.raises(InputError):
        auth_register_v1('testing123@unsw.au', 'password', '@ first ', '@ last ')
    
    with pytest.raises(InputError):
        auth_register_v1('testing567@unsw.au', 'password', 'first @ name', 'last @ name')

    with pytest.raises(InputError):
        auth_register_v1('testing890@unsw.au', 'password', 'first @@@' , 'last @@@ ') 

# Test registration of details was successful - if registration is successful then you can login 
def test_registration_successful():
    clear_v1()

    userid_1 = auth_register_v1('testing123@unsw.au', 'password', 'first1', 'last1') 
    userid_2 = auth_register_v1('testing567@unsw.au', 'password', 'first2', 'last2') 
    userid_3 = auth_register_v1('testing890@unsw.au', 'password', 'first3', 'last3') 

    assert auth_login_v1('testing123@unsw.au', 'password') == userid_1
    assert auth_login_v1('testing567@unsw.au', 'password') == userid_2
    assert auth_login_v1('testing890@unsw.au', 'password') == userid_3

    

