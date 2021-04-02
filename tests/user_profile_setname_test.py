import pytest
from src.auth import auth_register_v2
from src.user import user_profile_setname_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.helper import find_user, load_data


def test_auth_user_id_valid():
    clear_v1()

    with pytest.raises(AccessError):
        user_profile_setname_v2(100, 'firstname', 'lastname')

    clear_v1()


def test_first_name_incorrect_length():
    clear_v1()

    user_1 = auth_register_v2('test@unsw.au', 'password', 'first', 'last')

    with pytest.raises(InputError):
        user_profile_setname_v2(
            user_1['auth_user_id'], 'thisfirstnamecontainsspecialcharacters##^^&&**!!123123123', 'lastname')

    clear_v1()


def test_last_name_incorrect_length():
    clear_v1()

    user_1 = auth_register_v2('test@unsw.au', 'password', 'first', 'last')

    with pytest.raises(InputError):
        user_profile_setname_v2(user_1['auth_user_id'], 'firstname',
                                'thislastnamecontainsspecialcharacters##^^&&**!!123123123')

    clear_v1()


def test_successful_setname():
    clear_v1()

    user_1 = auth_register_v2('test@unsw.au', 'password', 'first', 'last')
    user_profile_setname_v2(user_1['auth_user_id'], 'firstname', 'lastname')

    data = load_data()
    user_1_details = find_user(user_1['auth_user_id'], data)

    assert user_1_details['first_name'] == 'firstname'
    assert user_1_details['last_name'] == 'lastname'

    clear_v1()
