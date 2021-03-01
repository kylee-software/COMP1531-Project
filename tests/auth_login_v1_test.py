import pytest 

# Test exception - Email given is not valid (wrong format)
def test_given_invalid_email(): 
    with pytest.raises(InputError) 

# Test exception - Email given doesn't match a user's email (email doesn't exist)
def test_given_email_nonexistent():
    with pytest.raises(InputError)

# Test exception - password given is not correct
def test_password_incorrect():
    with pytest.raises(InputError)

# Test where auth_user_id given as email and password given are correct
def correct_login_details_given(): 
    with pytest.raises(InputError)
     
