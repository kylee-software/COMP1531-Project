# Just a draft of the layout, variable types are incorrect at the moment

register_info = {'email1@gmail.com': {'password': 'string1',
                                      'user_id': 'integers'},
                 'email2@gmail.com': {'password': 'string2',
                                      'user_id': 'integers'}
                 }

# user_ids are integers
user_info = {'user_id_1': {'first_name': 'first_name',
                           'last_name': 'last_name',
                           'handle': 'string',
                           'global_owner_status': 'boolean'},
             'user_id_2': {'first_name': 'first_name',
                           'last_name': 'last_name',
                           'handle': 'string',
                           'global_owner_status': 'boolean'}
             }

# user_ids are integers
channel_info = {'channel_id_1': {'name': 'channel_name',
                                 'members': {'user_id_1', 'user_id_2', 'user_id_3'},
                                 'messages': 'string'},
                'channel_id_2': {'name': 'channel_name',
                                 'members': {'user_id_1', 'user_id_2', 'user_id_3'},
                                 'messages': 'string'}
                }


