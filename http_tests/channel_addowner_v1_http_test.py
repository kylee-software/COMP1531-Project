import requests
from src import config
from src.helper import is_valid_token


def test_invalid_channel():
    requests.delete(config.url + '/clear/v1')
    admin = requests.post(config.url + '/auth/register/v2',
                          json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    member = requests.post(config.url + '/auth/register/v2',
                           json={'email': 'test1@unsw.au', 'password': 'password1', 'name_first': 'test1', 'name_last': 'last1'})
    admin_details = admin.json()
    member_details = member.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin_details['token'], 'channel_id': 1, 'u_id': member_details['auth_user_id']})
    assert addowner.status_code == 400


def test_user_nonexistent():
    requests.delete(config.url + '/clear/v1')
    admin = requests.post(config.url + '/auth/register/v2',
                          json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    admin_details = admin.json()
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin_details['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin_details['token'], 'channel_id': channel_id['channel_id'], 'u_id': 10})
    assert addowner.status_code == 400


def test_user_already_owner():
    requests.delete(config.url + '/clear/v1')
    admin = requests.post(config.url + '/auth/register/v2',
                          json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    admin_details = admin.json()
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin_details['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin_details['token'], 'channel_id': channel_id['channel_id'], 'u_id': admin_details['auth_user_id']})
    assert addowner.status_code == 400


def test_not_owner_of_channel_or_dreams():
    requests.delete(config.url + '/clear/v1')
    admin = requests.post(config.url + '/auth/register/v2',
                          json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    member_1 = requests.post(config.url + '/auth/register/v2',
                             json={'email': 'test1@unsw.au', 'password': 'password1', 'name_first': 'test1', 'name_last': 'last1'})
    member_2 = requests.post(config.url + '/auth/register/v2',
                             json={'email': 'test2@unsw.au', 'password': 'password2', 'name_first': 'test2', 'name_last': 'last2'})
    admin_details = admin.json()
    member_1_details = member_1.json()
    member_2_details = member_2.json()
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin_details['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': member_1_details['token'], 'channel_id': channel_id['channel_id'], 'u_id': member_2_details['auth_user_id']})
    assert addowner.status_code == 403


def test_successful_addowner():
    requests.delete(config.url + '/clear/v1')

    admin = requests.post(config.url + '/auth/register/v2',
                          json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'test123', 'name_last': 'last123'})
    member_1 = requests.post(config.url + '/auth/register/v2',
                             json={'email': 'test1@unsw.au', 'password': 'password1', 'name_first': 'test1', 'name_last': 'last1'})
    admin_details = admin.json()
    member_1_details = member_1.json()
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin_details['token'], 'name': 'channel_1', 'is_public': True})
    channel_details = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin_details['token'], 'channel_id': channel_details['channel_id'], 'u_id': member_1_details['auth_user_id']})
    assert addowner.status_code == 200
