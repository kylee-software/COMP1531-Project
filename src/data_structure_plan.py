

# user_info = [ {'first_name' : string,
#                'last_name' : string,
#                'email' : string,
#                'user_id' : int?,
#                'password' : string,
#                'global_owner_status' : boolean,
#                'handle' : string,        
#               }, 
#               {....}, ....
#             ]
#    --> authorisation? how do you become unauthorised?

# channel_info = [ {'name': string,
#                   'channel_id':int?,
#                   'public_status': boolean (false indicates private),
#                   'members' : [ { 'user_id':int?, 
#                                   'channel_owner_status':boolean,
#                               },...],   
#                   'messages':[strings -> use insert function to add new message to start],
#                   }]

#   --> assuming owners will also be in the all_members return