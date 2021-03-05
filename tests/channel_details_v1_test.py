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
    return auth_register_v1(email,password,firstname, lastname)

@pytest.fixture
def create_channel(is_public):
    name = "Testchannel"
    user_id = auth_register_v1("channelcreator@gmail.com", "TestTest1", "first", "last")
    return channels_create_v1(user_id, name, is_public)

@pytest.fixture
def create_user_output(email, password, firstname, lastname, handle):
    return {'u_id':auth_login_v1(email, password), "email":email, 'name_first':firstname,'name_last':lastname,'handle_str':handle,}

@pytest.fixture
def expected_output():
    name = "Testchannel"
    owner = create_user_output("channelcreator@gmail.com", "TestTest1", "first", "last", "firstlast")
    other_member = create_user_output("test2email@gmail.com", "TestTest2", "firstname2", "lastname2", "firstname2lastname2")
    return {'name':name,'owner_members':[owner],'all_members':[owner, other_member]}


def test_valid_case():
    clear_v1()
    channel_id = create_channel(True)
    owner_id = auth_login_v1("channelcreator@gmail.com", "TestTest1")
    user_id2 = create_user()
    channel_join_v1(user_id2, channel_id)
    assert channel_details_v1(user_id2, channel_id) == expected_output()
    assert channel_details_v1(owner_id, channel_id) == expected_output()

    
def test_invalid_channel_id():
    clear_v1()
    user_id = create_user()
    with pytest.raises(InputError):
        channel_details_v1(user_id, 1)

#NOT IN SPECS:
def test_user_id_doesnt_exist():
    clear_v1()
    channel_id = create_channel(True)
    user_id = auth_login_v1("channelcreator@gmail.com", "TestTest1")
    user_id += user_id
    with pytest.raises(InputError):
        channel_details(user_id, channel_id)

def test_user_not_in_channel():
    clear_v1()
    channel_id = create_channel(True)
    user_id = create_user()
    with pytest.raises(AccessError):
        channel_details(user_id, channel_id)

# AccessError: auth_id is not part of channel
# want to check auth_id is in channel
# check auth_id that is not in channel
