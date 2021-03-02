# Just a draft of the layout, variable types are incorrect at the moment
user_info = [{'user_id': 'number1',
              'first_name': 'string',
              'last_name': 'string',
              'email': 'string',
              'password': 'string',
              'global_owner_status':'boolean',
              'handle': 'string'},
             {'user_id': 'number1',
              'first_name': 'string',
              'last_name': 'string',
              'email': 'string',
              'password': 'string',
              'global_owner_status': 'boolean',
              'handle': 'string',
              }
             ]

channel_info = [{'channel_id': 'id1',
                 'name': 'string',
                 'public_status': 'boolean',
                 'members': [{'user_id': 'id1',
                              'channel_owner_status': 'boolean'
                              }],
                 'messages': 'words'},
                {'channel_id': 'id1',
                 'name': 'string',
                 'public_status': 'boolean',
                 'members': [{'user_id': 'id1',
                              'channel_owner_status': 'boolean'
                              }],
                 'messages': 'words'
                 }
                ]

