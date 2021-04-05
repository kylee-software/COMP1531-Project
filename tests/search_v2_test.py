import pytest
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.error import AccessError, InputError
from src.message import message_edit_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.message import message_send_v2, message_senddm_v1
from src.channel import channel_messages_v2


@pytest.fixture(autouse=True)
def clear():
    clear_v1()
    yield
    clear_v1()


@pytest.fixture
def admin():
    return auth_register_v2('test@unsw.au', 'password1', 'first1', 'last1')


@pytest.fixture
def member():
    return auth_register_v2('test1@unsw.au', 'password2', 'first2', 'last2')


@pytest.fixture
def channel(admin):
    return channels_create_v2(admin['token'], 'channel_1', True)


@pytest.fixture
def dm(admin, member):
    return dm_create_v1(admin['token'], [member['auth_user_id']])


@pytest.fixture
def channel_messages(admin, channel):
    message_send_v2(admin['token'], channel['channel_id'],
                    'this is a message sent to the other user in the channel.')
    message_send_v2(admin['token'], channel['channel_id'],
                    'this is a message sent to the other user in the channel11111.')
    message_send_v2(admin['token'], channel['channel_id'],
                    'this is a message sent to the other user in the channel2222.')


@pytest.fixture
def dm_messages(admin, dm):
    message_senddm_v1(admin['token'], dm['dm_id'],
                      'this is a message sent to the other user.')
    message_senddm_v1(admin['token'], dm['dm_id'],
                      'this is a message sent to the other user.11111')
    message_senddm_v1(admin['token'], dm['dm_id'],
                      'this is a message sent to the other user.22222')


def test_invalid_token_dm(dm_message):
    invalid_token = 'invalidtoken123123'
    with pytest.raises(AccessError):
        message_edit_v2(
            invalid_token, dm_message['message_id'], 'this is an updated message in the dm.')


def test_invalid_token_channel(channel_message):
    invalid_token = 'invalidtoken123123'
    with pytest.raises(AccessError):
        message_edit_v2(
            invalid_token, channel_message, 'this is an updated message in the dm.')


def test_query_string_length_incorrect():
    with pytest.raises(InputError)
