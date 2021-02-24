

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

#alternative with channel_info --> 'members':[user_ids], 'owners':[user_ids],
#     --> need to make assumption about whether to add owner to members in this case

auth_user_id = 0

channel_info = [ {'name': "",
                   'channel_id': "",
                   'public_status': "",
                   'members' : [ { 'user_id': "", 
                                   'channel_owner_status': "",
                               },],   
                   'messages':[],
                   }]
