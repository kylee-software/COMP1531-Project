import requests
from src import config
from src.helper import create_token


def test_invalid_token():
    requests.delete(config.url + '/clear/v1')
    invalid_token = create_token(100, 10)
    setname_call = requests.put(config.url + '/user/profile/setname/v2',
                                json={'token': invalid_token, 'name_first': 'firstname', 'name_last': 'lastname'})
    assert setname_call.status_code == 400


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
