import pytest
from src.other import clear_v1
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.message import message_senddm_v1
from src.error import InputError, AccessError

@pytest.fixture
def token():
    clear_v1()
    # create a test user and return auth_id
    email = "testmail@gamil.com"
    password = "Testpass12345"
    token = auth_register_v2(email, password, "firstname", "lastname")['token']
    return token

@pytest.fixture
def dm_id(token):
    # create a public channel and return dm_id
    member1 = auth_register_v2("testmail@gamil1.com", "Testpass123456", "firstone", "lastone")['auth_user_id']
    member2 = auth_register_v2("testmail@gamil2.com", "Testpass1234567", "firsttwo", "lasttwo")['auth_user_id']
    dm_id = dm_create_v1(token, [member1, member2])['dm_id']
    return dm_id

@pytest.fixture
def unauthorised_user():
    email = "testmail3@gamil.com"
    password = "Testpass12345"
    token = auth_register_v2(email, password, "firstthree", "lastthree")['token']
    return token

def test_invalid_token(dm_id):
    with pytest.raises(AccessError):
        dm_messages_v1("invalid_token", dm_id, 0)

def test_invalid_dm_id(token, dm_id):
    with pytest.raises(InputError):
        dm_messages_v1(token, dm_id + 1, 0)

def test_unauthorised_user(unauthorised_user, dm_id):
    # Test an user that does not belong to the dm with the given dm_id
    with pytest.raises(AccessError):
        dm_messages_v1(unauthorised_user, dm_id, 0)

def test_invalid_start(token, dm_id):
    # this fail because no message is being sent to the dm yet
    with pytest.raises(InputError):
        dm_messages_v1(token, dm_id, 51)

def test_last_message(token, dm_id):
    # Test if end = -1 when there are no more messages to load after the current return
    message_senddm_v1(token, dm_id, "Hi, everyone!")
    end = dm_messages_v1(token, dm_id, 0)['end']
    assert end == -1

def test_more_messages(token, dm_id):
    count = 60
    while count >= 0:
        message_senddm_v1(token, dm_id, f"{count}")
        count -= 1

    # Test first 50 newest messages
    message_1 = dm_messages_v1(token, dm_id, 0)['messages'][49]['message']
    assert message_1 == "49"
    # Test the first message in the returned message dictionary
    message_2 = dm_messages_v1(token, dm_id, 10)['messages'][0]['message']
    assert message_2 == "10"
    # Test the second message in the returned message dictionary
    message_3 = dm_messages_v1(token, dm_id, 30)['messages'][1]['message']
    assert message_3 == '31'
    # Test the earliest message that was sent to the dm
    message_4 = dm_messages_v1(token, dm_id, 60)['messages'][0]['message']
    assert message_4 == '60'

    clear_v1()

