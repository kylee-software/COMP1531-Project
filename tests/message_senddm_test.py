import pytest
from src.other import clear_v1, notifications_get_v1
from src.auth import auth_register_v2, auth_login_v2
from src.dm import dm_create_v1
from src.error import InputError, AccessError
from src.message import message_senddm_v1
from src.helper import is_valid_token, find_user, load_data

@pytest.fixture
def user1():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user2():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def user3():
    email = "test3email@gmail.com"
    password = "TestTest3"
    firstname = "firstname3"
    lastname = "lastname3"
    return auth_register_v2(email,password,firstname, lastname)

@pytest.fixture
def clear():
    clear_v1()

def test_message_too_long(clear, user1, user2):
    dm = dm_create_v1(user1['token'], [user2['auth_user_id']])
    with pytest.raises(InputError):
        message_senddm_v1(user1['token'], dm['dm_id'], "Toolong"*500)
    clear_v1()

def test_user_not_in_dm(clear, user1, user2, user3):
    dm = dm_create_v1(user1['token'], [user2['auth_user_id']])
    with pytest.raises(AccessError):
        message_senddm_v1(user3['token'], dm['dm_id'], "Message")
    clear_v1()

def test_invalid_token(clear, user1, user2):
    dm = dm_create_v1(user1['token'], [user2['auth_user_id']])
    with pytest.raises(AccessError):
        message_senddm_v1('invalid.token.input', dm['dm_id'], "Message")
    clear_v1()

def test_send_message(clear, user1, user2):
    dm = dm_create_v1(user1['token'], [user2['auth_user_id']])
    assert isinstance(message_senddm_v1(user1['token'], dm['dm_id'], "Message")['message_id'], int)
    # To more thoroughly test the data is saved correctly the following will be used once dm messages has been implemented
    #assert dm_messages_v1(user1['token'], dm['dm_id'], 0) == {['Message'], 0, -1}
    pass
    clear_v1()

# will assume an Input error is raised if the id is invalid
def test_dm_id_invalid(clear, user1, user2):
    dm = dm_create_v1(user1['token'], [user2['auth_user_id']])
    with pytest.raises(InputError):
        message_senddm_v1(user1['token'], dm['dm_id']+1, "Message")
    clear_v1()

def test_multiple_messages(clear, user1, user2):
    dm = dm_create_v1(user1['token'], [user2['auth_user_id']])
    assert isinstance(message_senddm_v1(user1['token'], dm['dm_id'], "Message")['message_id'], int)
    assert isinstance(message_senddm_v1(user1['token'], dm['dm_id'], "Message2")['message_id'], int)
    assert isinstance(message_senddm_v1(user1['token'], dm['dm_id'], "Message3")['message_id'], int)
    # To more thoroughly test the data is saved correctly the following will be used once dm messages has been implemented
    #assert dm_messages_v1(user1['token'], dm['dm_id'], 0) == {['Message', 'Message2', 'Message3'], 0, -1}
    pass

def test_tagging(clear, user1, user2):
    dm = dm_create_v1(user1['token'], [user2['auth_user_id']])
    assert isinstance(message_senddm_v1(user1['token'], dm['dm_id'], "Message @firstname2lastname2")['message_id'], int)

def test_notification_message(clear, user1, user2):
    dm = dm_create_v1(user1['token'], [user2['auth_user_id']] + [user1['auth_user_id']])
    message = 'test message @firstname2lastname2'
    message_senddm_v1(user1['token'], dm['dm_id'], message)
    data = load_data()
    user = next(u for u in data['users'] if u['user_id'] == user2['auth_user_id'])
    print(user)

    user_handle = find_user(is_valid_token(user1['token'])['user_id'], data)['account_handle']
    notif = notifications_get_v1(user2['token'])
    dm_name = dm['dm_name']
    
    assert len(notif['notifications']) == 1
    assert notif['notifications'][0]['channel_id'] == -1
    assert notif['notifications'][0]['dm_id'] == dm['dm_id']
    assert notif['notifications'][0]['notification_message'] == f"{user_handle} tagged you in {dm_name}: {message[:20]}"