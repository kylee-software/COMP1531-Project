import pytest


from src.error import AccessError
from src.channels import channels_create_v1, channels_listall_v1
from src.other import clear_v1
from src.auth import auth_register_v2


@pytest.fixture
def auth_user_id():
    return auth_register_v2("test@unsw.com", 'testPassword8', 'Test', "User")['auth_user_id']


@pytest.fixture
def names():
    return ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']


@pytest.fixture
def clear():
    clear_v1()

# create one channel with one member and
#  no messages and


def test_oneChannel(clear, auth_user_id):
    channels_create_v1(auth_user_id, 'testChannel01', False)
    channelDict = channels_listall_v1(auth_user_id)
    assert len(channelDict['channels']) == 1
    clear_v1()

# test if there are no channels


def test_noChannels(clear, auth_user_id):
    assert channels_listall_v1(auth_user_id) == {'channels': []}
    clear_v1()

# test with multiple channels and public to true
# test with multiple channels


def test_fiveChannels_public(clear, auth_user_id, names):
    for name in names:
        channels_create_v1(auth_user_id, name, True)
    channelDict = channels_listall_v1(auth_user_id)
    assert len(channelDict['channels']) == 5
    clear_v1()

# test with multiple channels


def test_fiveChannels(clear, auth_user_id, names):
    for values in names:
        channels_create_v1(auth_user_id, values, False)
    channelDict = channels_listall_v1(auth_user_id)
    assert len(channelDict['channels']) == 5
    clear_v1()


def test_invalid_authId(clear):
    auth_user_id = 4
    with pytest.raises(AccessError):
        channels_listall_v1(auth_user_id)
    clear_v1()
