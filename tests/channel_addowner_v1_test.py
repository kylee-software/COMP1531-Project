import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_addowner_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.helper import is_user_in_channel, load_data, find_user_channel_owner_status, save_data


def test_invalid_channel():
    clear_v1()

    admin = auth_register_v1('test@unsw.au', 'password1', 'first1', 'last1')
    member = auth_register_v1('test1@unsw.au', 'password2', 'first2', 'last2')
    with pytest.raises(InputError):
        channel_addowner_v1(admin['auth_user_id'], 1, member['auth_user_id'])

    clear_v1()


def test_user_nonexistent():
    clear_v1()

    admin = auth_register_v1('test@unsw.au', 'password', 'first', 'last')
    channel_id = channels_create_v1(admin['auth_user_id'], 'channel_1', True)
    with pytest.raises(InputError):
        channel_addowner_v1(admin['auth_user_id'],
                            channel_id['channel_id'], 10)

    clear_v1()


def test_user_already_owner():
    clear_v1()
    admin = auth_register_v1('test@unsw.au', 'password', 'first', 'last')
    channel_id = channels_create_v1(admin['auth_user_id'], 'channel_1', True)
    with pytest.raises(InputError):
        channel_addowner_v1(admin['auth_user_id'],
                            channel_id['channel_id'], admin['auth_user_id'])

    clear_v1()


def test_not_owner_of_channel_or_dreams():
    clear_v1()

    admin_1 = auth_register_v1('test@unsw.au', 'password', 'first', 'last')
    member_1 = auth_register_v1(
        'test2@unsw.au', 'password2', 'first2', 'last2')
    member_2 = auth_register_v1(
        'test3@unsw.au', 'password3', 'first3', 'last3')
    channel_id = channels_create_v1(admin_1['token'], 'channel_1', True)
    with pytest.raises(AccessError):
        channel_addowner_v1(member_1['auth_user_id'],
                            channel_id['channel_id'], member_2['auth_user_id'])

    clear_v1()


def test_successful_addowner():
    clear_v1()

    data = load_data()

    admin = auth_register_v1('test@unsw.au', 'password1', 'first1', 'last1')
    member = auth_register_v1('test1@unsw.au', 'password2', 'first2', 'last2')
    channel_id = channels_create_v1(admin['token'], 'channel_1', True)
    channel_addowner_v1(
        admin['auth_user_id'], channel_id['channel_id'], member['auth_user_id'])

    save_data(data)

    assert is_user_in_channel(
        channel_id['channel_id'], member['auth_user_id'], data)
    assert find_user_channel_owner_status(
        channel_id['channel_id'], member['auth_user_id'], data) == 1

    clear_v1()
