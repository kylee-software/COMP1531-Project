import requests
from src import config
from src.helper import is_valid_token, create_token


def test_dm_not_valid():
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

    dm_1 = requests.post(config.url + '/dm/create/v1',
                         json={'token': admin_details['token'], 'u_ids': member_list})

    member_2_leave = requests.post(
        config.url + '/dm/leave/v1', json={'token': member_2_details['token'], 'dm_id': 1000})

    assert member_2_leave.status_code == 400


def test_auth_user_not_dm_member():
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

    dm_1 = requests.post(config.url + '/dm/create/v1',
                         json={'token': admin_details['token'], 'u_ids': member_list})

    invalid_token = create_token(3000, 300)

    not_member_of_dm = requests.post(
        config.url + '/dm/leave/v1', json={'token': invalid_token, 'u_ids': member_list})

    assert not_member_of_dm.status_code == 403


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

    dm_1 = requests.post(config.url + '/dm/create/v1',
                         json={'token': admin_details['token'], 'u_ids': member_list})

    dm_1_id = dm_1.json()
    dm_leave_success = requests.post(
        config.url + '/dm/leave/v1', json={'token': member_2_details['token'], 'dm_id': dm_1_id['dm_id']})

    assert dm_leave_success.status_code == 200
