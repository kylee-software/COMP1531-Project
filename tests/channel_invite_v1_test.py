import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

#Need to make a decision about global owners and whether they have access

@pytest.fixture
def create_user1():
    email = "test1email@gmail.com"
    password = "TestTest1"
    firstname = "firstname1"
    lastname = "lastname1"
    return auth_register_v1(email,password,firstname, lastname)['auth_user_id']

@pytest.fixture
def create_user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email,password,firstname, lastname)['auth_user_id']

@pytest.fixture
def create_channel(is_public):
    name = "Testchannel"
    user_id = auth_register_v1("channelcreator@gmail.com", "TestTest", "channelcreator", "last")
    return channels_create_v1(user_id, name, is_public)['channel_id']

#input errors:
#channel id is not valid
def test_invalid_channel_id():
    clear_v1()
    channel_id = create_channel(True)
    clear_v1()
    user_id_1 = create_user1()
    user_id_2 = create_user2()
    
    with pytest.raises(InputError):
        channel_invite_v1(user_id_1, channel_id, user_id_2)

# u id is not valid
def test_invalid_user_id():
    clear_v1()
    user_id_1 = create_user1()
    clear_v1()
    channel_id = create_channel(True)
    auth_user_id = auth_login_v1("channelcreator@gmail.com", "TestTest")['auth_user_id']
    
    with pytest.raises(InputError):
        channel_invite(auth_user_id, channel_id, user_id_1)
#access errors
#auth user not in channel
def test_unauthorised_user():
    clear_v1()
    user_id_1 = create_user1()
    user_id_2 = create_user2()
    channel_id = create_channel(True)

    with pytest.raises(AccessError):
        channel_invite_v1(user_id_2, channel_id, user_id_1)

def test_all_valid():
    clear_v1()
    user_id_1 = create_user1()
    channel_id = create_channel(True)
    auth_user_id = auth_login_v1("channelcreator@gmail.com", "TestTest")['auth_user_id']

    assert channel_invite_v1(auth_user_id, channel_id, user_id_1) == {}