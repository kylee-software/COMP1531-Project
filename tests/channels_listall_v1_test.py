import pytest


from src.channels import channels_create_v1, channels_listall_v1
from src.other import clear_v1
from src.auth import auth_register_v1

##what tests do are needed for this?
##I am not usre

##create one channel with one member and
#  no messages and
def test_oneChannel_oneMember_noMessages(auth_user_id):
    clear_v1()
    auth_user_id = auth_register_v1("test@test.unsw.com", 'testPassword8', 'Test', "User")
    channels_create_v1(auth_user_id, 'testChannel01', False)
    assert len(channels_listall_v1(auth_user_id)) == 1
    """assert channels_listall_v1(auth_user_id) == [ {'name': "testChannel01",
                                                            'channel_id': 1,
                                                            'public_status': False,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            }]"""

##test if there are no channels
def test_noChannel(auth_user_id):
    clear_v1()
    assert channels_listall_v1(auth_user_id) == []

##test with multiple channels and public to true
##test with multiple channels 
def test_fiveChannels_oneMember_noMessages_public(auth_user_id):
    clear_v1()
    auth_user_id = auth_register_v1("test@test.unsw.com", 'testPassword8', 'Test', "User")
    names = ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']
    for name in names:
        channels_create_v1(auth_user_id, name, True)
    assert len(channels_listall_v1(auth_user_id)) == 5
    """assert channels_listall_v1(auth_user_id) == [ {'name': "testChannel01",
                                                            'channel_id': 1,
                                                            'public_status': True,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },

                                                        {'name': "testChannel02",
                                                            'channel_id': 2,
                                                            'public_status': True,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },

                                                        {'name': "testChannel03",
                                                            'channel_id': 3,
                                                            'public_status': True,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },

                                                        {'name': "testChannel04",
                                                            'channel_id': 4,
                                                            'public_status': True,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },

                                                        {'name': "testChannel05",
                                                            'channel_id': 5,
                                                            'public_status': True,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },
                                                            
                                                        ]"""

##test with multiple channels 
def test_fiveChannels_oneMember_noMessages(auth_user_id):
    clear_v1()
    auth_user_id = auth_register_v1("test@test.unsw.com", 'testPassword8', 'Test', "User")
    names = ['testChannel01', 'testChannel02', 'testChannel03', 'testChannel04', 'testChannel05']
    for values in names:
        channels_create_v1(auth_user_id, values, False)
    assert len(channels_listall_v1(auth_user_id)) == 5
    """assert channels_listall_v1(auth_user_id) == [ {'name': "testChannel01",
                                                            'channel_id': 1,
                                                            'public_status': False,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },

                                                        {'name': "testChannel02",
                                                            'channel_id': 2,
                                                            'public_status': False,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },

                                                        {'name': "testChannel03",
                                                            'channel_id': 3,
                                                            'public_status': False,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },

                                                        {'name': "testChannel04",
                                                            'channel_id': 4,
                                                            'public_status': False,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },

                                                        {'name': "testChannel05",
                                                            'channel_id': 5,
                                                            'public_status': False,
                                                            'members' : [ { 'user_id': auth_user_id, 
                                                                            'channel_owner_status': True,
                                                                        },],   
                                                            'messages':[],
                                                            },
                                                            
                                                        ]"""
                                                            
                                                            





