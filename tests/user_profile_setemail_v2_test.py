import pytest
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import InputError, AccessError
from src.user import user_profile_setemail_v2

@pytest.fixture
def user():
    email = "testmail@gmail.com"
    password = "Testpass1"
    first_name = "firstone"
    last_name = "lastone"
    token = auth_register_v2(email, password, first_name, last_name)['token']
    return token

def test_invalid_token():
    with pytest.raises(AccessError):
        user_profile_setemail_v2("invalid_token", "testemail@gmail.com")

def test_invalid_email(user):
    with pytest.raises(InputError):
        user_profile_setemail_v2(user, "testemail.com")

def test_email_existed(user):
    with pytest.raises(InputError):
        user_profile_setemail_v2(user, "testmail@gmail.com")

def test_correct_setup(user):
    user_profile_setemail_v2(user, "newemail@gmail.com")
    with pytest.raises(InputError):
        user_profile_setemail_v2(user, "newemail@gmail.com") # means email is set to the new email
    clear_v1()


