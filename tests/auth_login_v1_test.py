import pytest
from src.auth import auth_login_v2, auth_register_v2
from src.other import clear_v1
from src.error import InputError
from src.helper import is_valid_token

# Test exception - Email given is not valid (wrong format)


def test_invalid_email():
    clear_v1()

    invalid_email_1 = '@unsw.edu.au'
    with pytest.raises(InputError):
        auth_login_v2(invalid_email_1, 'password')

    invalid_email_2 = 'test@.au'
    with pytest.raises(InputError):
        auth_login_v2(invalid_email_2, 'password')

    invalid_email_3 = 'test.unsw.edu.au'
    with pytest.raises(InputError):
        auth_login_v2(invalid_email_3, 'password')

    invalid_email_4 = 'test_special!!!@unsw.au'
    with pytest.raises(InputError):
        auth_login_v2(invalid_email_4, 'password')

    clear_v1()

# Test exception - Email given does not match a user's email (email doesn't exist)


def test_email_nonexistent():
    clear_v1()

    auth_register_v2('testing123@unsw.au', 'password', 'first123', 'last123')
    with pytest.raises(InputError):
        auth_login_v2('testfail1@unsw.au', 'password')

    auth_register_v2('testing567@unsw.au', 'password', 'first567', 'last567')
    with pytest.raises(InputError):
        auth_login_v2('testfail2@unsw.au', 'password')

    auth_register_v2('testing890@unsw.au', 'password', 'first890', 'last890')
    with pytest.raises(InputError):
        auth_login_v2('testfail3@unsw.au', 'password')

    clear_v1()

# Test exception - password given is not correct


def test_password_incorrect():
    clear_v1()

    auth_register_v2('testing123@unsw.au', 'password', 'first123', 'last123')
    with pytest.raises(InputError):
        auth_login_v2('testing123@unsw.au', 'failed123')

    auth_register_v2'testing567@unsw.au', 'password', 'first567', 'last567')
    with pytest.raises(InputError):
        auth_login_v2('testing567@unsw.au', 'failed567')

    auth_register_v2('testing890@unsw.au', 'password', 'first890', 'last890')
    with pytest.raises(InputError):
        auth_login_v2('testing890@unsw.au', 'failed890')

    clear_v1()

# Test - email and password given are correct


def test_correct_login_details():
    clear_v1()

    userid_1=auth_register_v2(
        'testing123@unsw.au', 'password', 'first123', 'last123')
    assert is_valid_token(userid_1['token'])

    clear_v1()
