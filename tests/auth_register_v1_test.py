import pytest

# Test exception - Email entered is not valid (wrong format)
def test_given_email_is_invalid():
    pass 

# Test exception - Email entered already exists (belongs to an existing user)
def test_email_already_exists():
    pass 

# Test exception - Password given is less than 6 Characters
def test_password_incorrect_length():
    pass 

# Test exception - First name given is between 1 and 50 inclusive 
def test_first_name_valid_length():
    pass 

# Test exception - Last name given is between 1 and 50 inclusive 
def test_last_name_valid_length():
    pass 

# Test if email stored correctly in dictionary 
def test_email_stored_in_dictionary():
    pass 

# Test if first name is stored correctly in dictionary
def test_first_name_stored_in_dictionary():
    pass 

# Test if last name is stored correctly in dictionary
def test_if_last_name_stored_in_dictionary():
    pass 

# Test if password is stored correctly in dictionary 
def test_password_stored_in_dictionary():
    pass 


# Tests for handle - no @ or whitespace, 20 characters only, Q - in the case where we need to add numbers to handles as the handle already exists, is it allowed to go over the 20 character limiit?
# Need clarification on names and handles - special characters, are @ and whitespace allowed in names, are special characters like #, _, -, $, % or \ allowed in names and handles? 
# Are numbers allowed in first or last names and are numbers in names given allowed in handles?