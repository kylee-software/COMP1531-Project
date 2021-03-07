import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

@pytest.fixture
def create_user():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v1(email,password,firstname, lastname)["auth_user_id"]

@pytest.fixture
def create_channel():
    name = "Testchannel"
    user_id = auth_register_v1("channelcreator@gmail.com", "TestTest1", "first", "last")["auth_user_id"]
    return channels_create_v1(user_id, name, True)

@pytest.fixture
def clear():
    clear_v1()

def create_user_output(email, password, firstname, lastname, handle):
    return {'u_id':auth_login_v1(email, password), "email":email, 'name_first':firstname,'name_last':lastname,'handle_str':handle,}

def expected_output():
    name = "Testchannel"
    owner = create_user_output("channelcreator@gmail.com", "TestTest1", "first", "last", "firstlast")
    other_member = create_user_output("test2email@gmail.com", "TestTest2", "firstname2", "lastname2", "firstname2lastname2")
    return {'name':name,'owner_members':[owner],'all_members':[owner, other_member]}

def test_valid_case(clear, create_channel, create_user):
    owner_id = auth_login_v1("channelcreator@gmail.com", "TestTest1")["auth_user_id"]
    channel_join_v1(create_user, create_channel)
    assert channel_details_v1(create_user, create_channel) == expected_output()
    assert channel_details_v1(owner_id, create_channel) == expected_output()

def test_invalid_channel_id(clear, create_user):
    with pytest.raises(InputError):
        channel_details_v1(create_user, 1)


def test_user_not_in_channel(clear, create_channel, create_user):
    with pytest.raises(AccessError):
        channel_details(create_user, create_channel)

