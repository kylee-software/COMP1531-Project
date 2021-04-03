import pytest
from src.other import clear_v1
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.dm import dm_list_v1, dm_create_v1, dm_leave_v1
from src.helper import create_token


def test_dm_not_valid():
    clear_v1()

    user = auth_register_v2('test1@unsw.au', 'password1', 'first1', 'last1')

    with pytest.raises(InputError):
        dm_leave_v1(user['token'], 300)

    clear_v1()


def test_auth_user_not_dm_member():
    clear_v1()

    admin = auth_register_v2('test1@unsw.au', 'password1', 'first1', 'last1')
    member_1 = auth_register_v2(
        'test2@unsw.au', 'password2', 'first2', 'last2')
    member_2 = auth_register_v2(
        'test3@unsw.au', 'password3', 'first3', 'last3')

    member_list = []
    member_list.append(member_1['auth_user_id'])
    member_list.append(member_2['auth_user_id'])

    dm_1 = dm_create_v1(admin['token'], member_list)

    invalid_user = create_token(321321, 321)

    with pytest.raises(AccessError):
        dm_leave_v1(invalid_user, dm_1['dm_id'])

    clear_v1()


def test_success_case():
    clear_v1()

    admin = auth_register_v2('test1@unsw.au', 'password1', 'first1', 'last1')
    member_1 = auth_register_v2(
        'test2@unsw.au', 'password2', 'first2', 'last2')
    member_2 = auth_register_v2(
        'test3@unsw.au', 'password3', 'first3', 'last3')

    member_list = []
    member_list.append(member_1['auth_user_id'])
    member_list.append(member_2['auth_user_id'])

    dm_1 = dm_create_v1(admin['token'], member_list)

    dm_leave_v1(member_2['token'], dm_1['dm_id'])

    member_2_dm_list = dm_list_v1(member_2['token'])

    assert member_2_dm_list['dms'] == []

    clear_v1()
