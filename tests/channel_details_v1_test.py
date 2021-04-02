import pytest
from src.other import clear_v1
from src.auth import auth_register_v2, auth_login_v2
from src.channel import channel_join_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError


@pytest.fixture
def user1():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)


@pytest.fixture
def channel_id():
    name = "Testchannel"
    owner_id = auth_register_v2("channelcreator@gmail.com", "TestTest1", "first", "last")["auth_user_id"]
    return channels_create_v1(owner_id, name, True)['channel_id']


@pytest.fixture
def clear():
    clear_v1()

def test_valid_case(clear, channel_id, user1):
    owner_id = auth_login_v2("channelcreator@gmail.com", "TestTest1")
    channel_join_v1(user1['token'], channel_id)
    assert channel_details_v1(user1['token'], channel_id) == {
                                                        'name':"Testchannel",
                                                        'is_public':True,
                                                        'owner_members':[{
                                                                            'u_id':owner_id["auth_user_id"], 
                                                                            "email":"channelcreator@gmail.com", 
                                                                            'name_first':"first",
                                                                            'name_last':"last",
                                                                            'handle_str':"firstlast",
                                                                            },],
                                                        'all_members':[{
                                                                            'u_id':owner_id["auth_user_id"], 
                                                                            "email":"channelcreator@gmail.com", 
                                                                            'name_first':"first",
                                                                            'name_last':"last",
                                                                            'handle_str':"firstlast",
                                                                        }, 
                                                                        {
                                                                            'u_id':user1['auth_user_id'], 
                                                                            "email":"test2email@gmail.com", 
                                                                            'name_first':"firstname2",
                                                                            'name_last':"lastname2",
                                                                            'handle_str':"firstname2lastname2",
                                                                        },],
                                                        }
    assert channel_details_v1(owner_id['token'], channel_id) == {
                                                        'name':"Testchannel",
                                                        'is_public':True,
                                                        'owner_members':[{
                                                                            'u_id':owner_id["auth_user_id"], 
                                                                            "email":"channelcreator@gmail.com", 
                                                                            'name_first':"first",
                                                                            'name_last':"last",
                                                                            'handle_str':"firstlast",
                                                                            },],
                                                        'all_members':[{
                                                                            'u_id':owner_id["auth_user_id"], 
                                                                            "email":"channelcreator@gmail.com", 
                                                                            'name_first':"first",
                                                                            'name_last':"last",
                                                                            'handle_str':"firstlast",
                                                                        }, 
                                                                        {
                                                                            'u_id':user1['auth_user_id'], 
                                                                            "email":"test2email@gmail.com", 
                                                                            'name_first':"firstname2",
                                                                            'name_last':"lastname2",
                                                                            'handle_str':"firstname2lastname2",
                                                                        },],
                                                        }
    clear_v1() 

def test_invalid_channel_id(clear, user1):
    with pytest.raises(InputError):
        channel_details_v1(user1['token'], 1)
    clear_v1() 

def test_user_not_in_channel(clear, channel_id, user1):
    with pytest.raises(AccessError):
        channel_details_v1(user1['token'], channel_id)
    clear_v1() 

def test_invalid_token(clear, channel_id, user1):
    with pytest.raises(AccessError):
        channel_details_v1('bad.token.given', channel_id)
    clear_v1()

