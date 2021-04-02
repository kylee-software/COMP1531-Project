import requests
import pytest
from src import config
from src.helper import create_token, is_valid_token
from src.error import AccessError


def test_user_nonexistent_token():
    requests.delete(config.url + '/clear/v1')
    token = create_token(100, 10)
    setname_access_invalid = requests.put(config.url + '/user/profile/setname/v2',
                                          json={'token': token, 'name_first': 'firstname', 'name_last': 'lastname'})
    assert setname_access_invalid.status_code == 403


def test_first_name_incorrect_length():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    registration_details = registration.json()
    setname_call = requests.put(config.url + '/user/profile/setname/v2',
                                json={'token': registration_details['token'], 'name_first': 'thisfirstnamecontainsspecialcharacters##^^&&**!!123123123', 'name_last': 'lastname'})
    assert setname_call.status_code == 400


def test_last_name_incorrect_length():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    registration_details = registration.json()
    setname_call = requests.put(config.url + '/user/profile/setname/v2',
                                json={'token': registration_details['token'], 'name_first': 'firstname', 'name_last': 'thislastnamecontainsspecialcharacters##^^&&**!!123123123'})
    assert setname_call.status_code == 400


def test_successful_setname():
    requests.delete(config.url + '/clear/v1')
    registration = requests.post(config.url + '/auth/register/v2',
                                 json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    registration_details = registration.json()
    setname_call = requests.put(config.url + '/user/profile/setname/v2',
                                json={'token': registration_details['token'], 'name_first': 'firstname', 'name_last': 'lastname'})
    assert setname_call.status_code == 200
