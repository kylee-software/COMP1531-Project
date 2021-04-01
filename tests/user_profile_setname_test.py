import pytest
from src.auth import auth_register_v1
from src.user import user_profile_setname_v1
from src.error import InputError
from src.other import clear_v1


def test_auth_user_id_valid():
    clear_v1()

    user_1 = auth_register_v1('test@unsw.au', 'password', 'first', 'last')

    with pytest.raises(InputError):
        user_profile_setname_v1(100, 'firstname', 'lastname')

    clear_v1()


def test_first_name_incorrect_length():
    clear_v1()

    user_1 = auth_register_v1('test@unsw.au', 'password', 'first', 'last')

    with pytest.raises(InputError):
        user_profile_setname_v1(
            user_1['auth_user_id'], 'thisfirstnamecontainsspecialcharacters##^^&&**!!123123123', 'lastname')

    clear_v1()


def test_last_name_incorrect_length():
    clear_v1()

    user_1 = auth_register_v1('test@unsw.au', 'password', 'first', 'last')

    with pytest.raises(InputError):
        user_profile_setname_v1(user_1['auth_user_id'], 'firstname',
                                'thislastnamecontainsspecialcharacters##^^&&**!!123123123')

    clear_v1()


def test_successful_setname():
    clear_v1()

    user_1 = auth_register_v1('test@unsw.au', 'password', 'first', 'last')
    user_profile_setname_v1(user_1['auth_user_id'], 'firstname', 'lastname')

    assert user_1['first_name'] == 'firstname'
    assert user_1['last_name'] == 'lastname'

    clear_v1()
