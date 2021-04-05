# Assumptions For Iteration One

## admin_user_remove

- A global owner can remove themself
- Other user can not add the "removed user" to a channel or dm later
- if the user with u_id is the only owner of a channel, then we can not remove the user
- remove dms that the "remover user" are in if the user is the creator

## channel_join_v1

- if user tries to join a channel they are already in, nothing is done to the data store and the function simply returns successful (as they are in the channel)

## channel_invite_v1

- if user tries to invite someone to channel they are already in, nothing is done to the data store and the function returns successful
- if global owner is not in channel they also cannot invite users to the channel (they have no special power there)

## Channel_addowner_v1

- If the user to be added as a owner is not a member of the channel they are added as a member and their channel_owner_status is set to True

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

## channel/leave/v1:

- if the user trying to leave is the only owner, no other users will be made an owner in their place
- if the user trying to leave is the only member of the channel, the channel will not be deleted even if it is private (and therefore unjoinable)

## Functions without assumptions

- channel_details_v1
- auth_login_v1
- channel_messages_v2
- channels_create

## Dm/Invite

- You can't invite someone to a dm if they are already a member of that dm (raises InputError)

## message_send

- You are allowed to tag yourself in a message

## user/profile/v1
- Will not list removed users
## message share

- If the optional message plus the shared messaged together is over 1000 characters its too long and an input error is raised
- If the person sharing the message is not in the channel or dm the original message is from they are not authorised to share it and an access error is raised
- If either channel_id or dm_id is not -1 an input error will be raised

## user_profile_sethandle

- If you try to 'change' your handle to what it already is input error is raised (because the handle already exists)

## search_v2

- Matched queries means a message that contains a query string i.e The query is a substring of the message. (Exact match inclusive)

## channel_removeowner

- User id of the user who is having their ownership taking away remains a member of the channel
- Channel owner can remove their ownership themself

