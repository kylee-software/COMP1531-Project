import pytest

from src.data_structure_plan import auth_user_id, channel_info
import src.channels

##what tests do are needed for this?
##I am not usre

##create one channel with one member and
#  no messages and
def test_OneChannel_OneMember_NoMessages(auth_user_id):
    channels_create_v1(auth_user_id, 'test01', False)
    assert channels.channels_listall_v1(auth_user_id) == [ {'name': "test01",
                                                            'channel_id': 1,
                                                            'public_status': False,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            }]









