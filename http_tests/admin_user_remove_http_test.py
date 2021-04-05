import pytest
import requests
import json
from src import config


@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

@pytest.fixture
def user():
    email = "testmail@gamil.com"
    password = "Testpass123"
    first_name = "first"
    last_name = "last"

    token = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['token']

    return token


def test_invalid_input(clear, user):
    resp = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': user,
        'u_id': "ab",
    })

    status_code = resp.status_code
    assert status_code == 400


def test_admin_user_remove(clear):
    email1, email2 = "testmail1@gamil.com", "testmail2@gamil.com"
    password1, password2 = "Testpass12345", "Testpass12346"
    first_name1, first_name2 = "firstone", "firsttwo"
    last_name1, last_name2 = "lastone", "lasttwo"

    global_owner1 = requests.post(config.url + 'auth/register/v2', json={
        'email': email1,
        'password': password1,
        'name_first': first_name1,
        'name_last': last_name1
    }).json()

    global_owner2 = requests.post(config.url + 'auth/register/v2', json={
        'email': email2,
        'password': password2,
        'name_first': first_name2,
        'name_last': last_name2
    }).json()

    # Make global_owner2 to an owner of Dreams
    requests.post(config.url + "admin/userpermission/change/v1",
                  json={'token': global_owner1['token'], 'u_id': global_owner2['auth_user_id'],
                        'permission_id': 1})

    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': global_owner1['token'],
        'name': "channelName1",
        'is_public': True
    }).json()['channel_id']

    requests.post(config.url + 'channel/addowner/v1',
                  json={'token': global_owner1['token'],
                        'channel_id': channel_id,
                        'u_id': global_owner2['auth_user_id']})

    resp = requests.delete(config.url + 'admin/user/remove/v1', json={
        'token': global_owner1['token'],
        'u_id': global_owner2['auth_user_id'],
    })

    assert resp.json() == {}
