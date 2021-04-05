import pytest
from src.auth import auth_register_v2
from src.channel import channel_addowner_v1
from src.channels import channels_create_v2
from src.other import clear_v1
from src.error import InputError, AccessError
from src.helper import is_user_in_channel, load_data, find_user_channel_owner_status, save_data, create_token


@pytest.fixture()
def clear():
    clear_v1()


@pytest.fixture
def create_admin():
    admin = auth_register_v2('test@unsw.au', 'password1', 'first1', 'last1')
    return admin


@pytest.fixture
def create_member():
    member = auth_register_v2('test1@unsw.au', 'password2', 'first2', 'last2')
    return member

def test_invalid_channel(clear, create_admin, create_member):
    admin = create_admin
    member = create_member
    with pytest.raises(InputError):
        channel_addowner_v1(admin['auth_user_id'], 100, member['auth_user_id'])

    clear_v1()


def test_member_nonexistent(clear, create_admin):
    admin = create_admin
    channel_id = channels_create_v2(admin['token'], 'channel_1', True)
    with pytest.raises(InputError):
        channel_addowner_v1(admin['auth_user_id'],
                            channel_id['channel_id'], 10)

    clear_v1()


def test_user_already_owner(clear, create_admin):
    admin = create_admin
    channel_id = channels_create_v2(admin['token'], 'channel_1', True)
    with pytest.raises(InputError):
        channel_addowner_v1(admin['auth_user_id'],
                            channel_id['channel_id'], admin['auth_user_id'])

    clear_v1()


def test_not_owner_of_channel_or_dreams(clear, create_admin, create_member):
    admin_1 = create_admin
    member_1 = create_member
    member_2 = auth_register_v2(
        'test3@unsw.au', 'password3', 'first3', 'last3')
    channel_id = channels_create_v2(admin_1['token'], 'channel_1', True)
    with pytest.raises(AccessError):
        channel_addowner_v1(member_1['auth_user_id'],
                            channel_id['channel_id'], member_2['auth_user_id'])

    clear_v1()


def test_successful_addowner(clear, create_admin, create_member):
    admin = create_admin
    member = create_member
    channel_id = channels_create_v2(admin['token'], 'channel_1', True)
    channel_addowner_v1(
        admin['token'], channel_id['channel_id'], member['auth_user_id'])

    data = load_data()

    assert is_user_in_channel(
        channel_id['channel_id'], member['auth_user_id'], data)
    assert find_user_channel_owner_status(
        channel_id['channel_id'], member['auth_user_id'], data) == 1

    clear_v1()
