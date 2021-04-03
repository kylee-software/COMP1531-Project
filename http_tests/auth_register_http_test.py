import requests
from src import config
from src.helper import is_valid_token


def test_given_email_is_invalid():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test.unsw.edu.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    assert registration.status_code == 400


def test_email_already_exists():
    requests.delete(config.url + '/clear/v1')
    requests.post(config.url + '/auth/register/v2',
                  json={'email': 'test@unsw.edu.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test@unsw.edu.au', 'password': 'password2', 'name_first': 'test321', 'name_last': 'last321'})
    assert registration.status_code == 400


def test_password_incorrect_length():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test@unsw.edu.au', 'password': ' ', 'name_first': 'test123', 'name_last': 'last123'})
    assert registration.status_code == 400


def test_first_name_valid_length():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'thisfirstnameistoolongandcontainsspecialcharacters##^^&&**!!123123123', 'name_last': 'last123'})
    assert registration.status_code == 400


def test_last_name_valid_length():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'firstname', 'name_last': 'thislastnamecontainsspecialcharacters##^^&&**!!123123123'})
    assert registration.status_code == 400


def test_no_whitespace():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'first name', 'name_last': 'last name'})
    assert registration.status_code == 400


def test_no_at_symbol():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'firstn@me', 'name_last': 'l@stn@me'})
    assert registration.status_code == 400


def test_no_at_and_whitespace():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(
        config.url + '/auth/register/v2',
        json={'email': 'test@unsw.au', 'password': 'password', 'name_first': '@ first ', 'name_last': '@ last '})
    assert registration.status_code == 400


def test_registration_successful():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2', json={'email': 'test@unsw.au',
                                                                         'password': 'password', 'name_first': 'firstname', 'name_last': 'lastname'})
    registration_details = registration.json()
    assert registration.status_code == 200
    assert is_valid_token(registration_details['token'])
