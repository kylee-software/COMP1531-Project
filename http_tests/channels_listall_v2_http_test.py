import pytest
import requests
from src import config

@pytest.fixture
def token():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    resp = requests.post(config.url + '/auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    return resp['token']

@pytest.fixture
def names():
    return ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

def test_no_channels(clear, token):
    returnDict = requests.get(config.url + '/channels/listall/v2', params={'token' : token})
    assert returnDict.json()['channels'] == []


def test_lists_a_single_channel(clear,token):
    requests.post(config.url + 'channels/create/v2', json={
        'token': token,
        'name': "testChnanel01",
        'is_public': True
    })
    returnDict = requests.get(config.url + '/channels/listall/v2', params={'token' : token})
    assert len(returnDict.json()['channels']) == 1


def test_can_see_five_channels(clear, token, names):
    for name in names:
        requests.post(config.url + 'channels/create/v2', json={'token': token,
            'name': name,
            'is_public': True
        })
    returnDict = requests.get(config.url + '/channels/listall/v2', params={'token' : token})
    assert len(returnDict.json()['channels']) == 5

def test_can_see_five_private_channels(clear, token, names):
    for name in names:
        requests.post(config.url + 'channels/create/v2', json={'token': token,
            'name': name,
            'is_public': False
        })
    returnDict = requests.get(config.url + '/channels/listall/v2', params={'token' : token})
    assert len(returnDict.json()['channels']) == 5
        
def test_invalid_token(clear):
    token = 4
    response = requests.get(config.url + '/channels/listall/v2', params={'token' : token})
    assert response.status_code == 403


