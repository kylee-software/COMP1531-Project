import requests
from src import config
from src.helper import is_valid_token

# Test that email is a valid format


def test_invalid_email():
    requests.delete(f"{config} /clear/v1")
    login_call = requests.post(f"{config}/auth/login/v2",
                               json={'email': 'testing.unsw.au', 'password': 'password'})
    assert login_call.status_code == 400

# Test that the email given belongs to the user


def test_email_nonexistent():
    requests.delete(f"{config} /clear/v1")
    login_call = requests.post(f"{config}/auth/login/v2",
                               json={'email': 'testing123@unsw.au', 'password': 'password'})
    assert login_call.status_code == 400

# Test that the password given belongs to the user and is correct


def test_password_incorrect():
    requests.delete(f"{config} /clear/v1")
    requests.post(f"{config}/auth/register/v2",
                  json={'email': 'testing123@unsw.au', 'password': 'password', 'name_first': 'testing123', 'name_last': 'last123'})
    login_call = requests.post(f"{config}/auth/login/v2",
                               json={'email': 'testing123@unsw.au', 'password': 'failed123'})
    assert login_call.status_code == 400

# Test that email and password given is correct


def test_correct_login_details():
    requests.delete(f"{config} /clear/v1")
    registration = requests.post(f"{config}/auth/register/v2",
                                 json={'email': 'testing123@unsw.au', 'password': 'password', 'name_first': 'testing123', 'name_last': 'last123'})
    login_call = requests.post(f"{config}/auth/login/v2",
                               json={'email': 'testing123@unsw.au', 'password': 'password'})
    login_details = login_call.json()
    registration_details = registration.json()
    assert login_call.status_code == 200
    assert is_valid_token(login_details['token'])
    assert registration_details['auth_user_id'] == login_details['auth_user_id']
