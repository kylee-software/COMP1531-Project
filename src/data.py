
data = {'users': [], 'channels':[], 'dms':[]}

# users =     [ {'first_name' : string,
#                'last_name' : string,
#                'email' : string,
#                'user_id' : int?,
#                'password' : string,
#                'global_owner_status' : boolean,
#                'handle' : string,        
#               }, 
#               {....}, ....
#             ]

# channels =    [ {'name': string,
#                   'channel_id':int?,
#                   'public_status': boolean (false indicates private),
#                   'members' : [ { 'user_id':int?, 
#                                   'channel_owner_status':boolean,
#                               },...],   
#                   'messages':[strings -> use insert function to add new message to start],
#                   }]

# dms =     [   {'dm_id':int, 
#                'name':string, 
#                'members':[list of user_ids]
#                'messages':[ {'message_id':int,
#                              'message': string,
#                              }, {...}...
#                           ],
#               }   ]




]
