import pytest
from src.other import clear_v1
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.dm import dm_list_v1, dm_create_v1
from src.helper import create_token


def test_token_user_nonexistent():
    clear_v1()

    invalid_token = create_token(100000, 1000)

    with pytest.raises(AccessError):
        dm_list_v1(invalid_token)

    clear_v1()


def test_success_case():
    clear_v1()

    admin = auth_register_v2('test1@unsw.au', 'password1', 'first1', 'last1')
    member_1 = auth_register_v2(
        'test2@unsw.au', 'password2', 'first2', 'last2')
    member_2 = auth_register_v2(
        'test3@unsw.au', 'password3', 'first3', 'last3')

    members_list = []
    members_list.append(member_1['auth_user_id'])
    members_list.append(member_2['auth_user_id'])

    dm_create_v1(admin['token'], members_list)

    member_1_dm_list = dm_list_v1(member_1['token'])
    member_2_dm_list = dm_list_v1(member_2['token'])

    assert len(member_1_dm_list) == 1
    assert len(member_2_dm_list) == 1

    clear_v1()
