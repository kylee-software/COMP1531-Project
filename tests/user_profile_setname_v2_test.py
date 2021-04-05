import pytest
from src.auth import auth_register_v2
from src.user import user_profile_setname_v2, user_profile_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.helper import find_user, load_data


@pytest.fixture(autouse=True)
def clear():
    clear_v1()
    yield
    clear_v1()


@pytest.fixture
def create_user():
    user_1 = auth_register_v2('test@unsw.au', 'password', 'first', 'last')
    return user_1


def test_auth_user_id_valid():
    invalid_token = 'invalidtoken123456789'

    with pytest.raises(AccessError):
        user_profile_setname_v2(invalid_token, 'firstname', 'lastname')

    clear_v1()


def test_first_name_incorrect_length(create_user):

    user_1 = create_user

    with pytest.raises(InputError):
        user_profile_setname_v2(
            user_1['token'], 'thisfirstnamecontainsspecialcharacters##^^&&**!!123123123', 'lastname')


def test_last_name_incorrect_length(create_user):

    user_1 = create_user

    with pytest.raises(InputError):
        user_profile_setname_v2(user_1['token'], 'firstname',
                                'thislastnamecontainsspecialcharacters##^^&&**!!123123123')


def test_successful_setname(create_user):
    user_1 = create_user
    user_profile_setname_v2(user_1['token'], 'firstname', 'lastname')
    user_1_profile = user_profile_v2(
        user_1['token'], user_1['auth_user_id'])['user']
    assert user_1_profile['name_first'] == 'firstname'
    assert user_1_profile['name_last'] == 'lastname'
