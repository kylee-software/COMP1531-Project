# Assumptions For Iteration One

## channel_join_v1
- if user tries to join a channel they are already in, nothing is done to the data store and the function simply returns successful (as they are in the channel)

## channel_invite_v1
- if user tries to invite someone to channel they are already in, nothing is done to the data store and the function returns successful
- if global owner is not in channel they also cannot invite users to the channel (they have no special power there)

## channels_listall_v1
- channel_create works and creates correct channel names and id's
- only have to test for length of returns channels list
- auth_register works
- returns a dictionary with key 'channels' and value [] if no channels have been created
    
## channels_list_v1
- channel_create works and creates correct channel names and id's
- auth_register works
- returns a dictionary with key 'channels' and value [] if no channels have been created
- only testing user created channels for simplicity not joined channels as channel_join is assumed to be working

## channels_create_v2
- channel name can not be empty

## auth_register_v1
- Numbers and special characters except for '@' are allowed in names. Whitespace is not allowed in names.
- Though handles are only allowed to be 20 characters, where the handle is taken, adding numbers to the handle and going over 20 characters is allowed, in order to create a unique handle for the new user.
- The first and last name can be in uppercase and/or lowercase.
- Password may contain numbers, special characters and whitespace. 

## Functions without assumptions
- channel_details_v1
- auth_login_v1

## Dm/Invite
- You can't invite someone to a dm if they are already a member of that dm (raises InputError)
## message_send
- You are allowed to tag yourself in a message
