import requests
from src import config
from src.helper import is_valid_token, create_token


def test_auth_user_id_nonexistent():
    requests.delete(config.url + '/clear/v1')
    invalid_token = create_token(1000, 100)
    dm_list_call = requests.get(
        config.url + '/dm/list/v1', json={'token': invalid_token})
    assert dm_list_call.status_code == 403


def test_success_case():
    requests.delete(config.url + '/clear/v1')

    admin = requests.post(config.url + '/auth/register/v2', json={
                          'email': 'test1@unsw.au', 'password': 'password1', 'name_first': 'first1', 'name_last': 'last1'})
    member_1 = requests.post(config.url + '/auth/register/v2', json={
                             'email': 'test2@unsw.au', 'password': 'password2', 'name_first': 'first2', 'name_last': 'last2'})
    member_2 = requests.post(config.url + '/auth/register/v2', json={
                             'email': 'test3@unsw.au', 'password': 'password3', 'name_first': 'first3', 'name_last': 'last3'})

    admin_details = admin.json()
    member_1_details = member_1.json()
    member_2_details = member_2.json()

    member_list = []
    member_list.append(member_1_details['auth_user_id'])
    member_list.append(member_2_details['auth_user_id'])

    requests.post(config.url + '/dm/create/v1',
                  json={'token': admin_details['token'], 'u_ids': member_list})

    member_1_dm = requests.get(
        config.url + '/dm/list/v1', json={'token': member_1_details['token']})
    member_2_dm = requests.get(
        config.url + '/dm/list/v1', json={'token': member_2_details['token']})

    member_1_dm_list = member_1_dm.json()
    member_2_dm_list = member_2_dm.json()

    assert member_1_dm.status_code == 200
    assert member_2_dm.status_code == 200
    assert len(member_1_dm_list) == 1
    assert len(member_2_dm_list) == 1
