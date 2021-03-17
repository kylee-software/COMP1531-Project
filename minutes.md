## MEETING ONE (WEEK TWO 24/02/2021)
# Description
Weekly meeting in lab/after lab
# Date
24/02/2021 - Lab + meeting (10-12, 12-1) 
# Attendees
Sesi, Kylee, Michael, Isabelle 
# Scribe
Isabelle 
# Lab Time Notes (10-12pm)
Project management:
- Will each use the standups channel on teams at times that work for ourselves due to conflicting time commitments 
- Have set up boards on git to assign different functions to different people and keep track of what??s being worked on 

Project:
- 12 auth, channel, channels functions in the starter code vs 9 in the table description ?? 
- Which ones do we do  
- Need to make 12 merge requests all up 
- Errors: covered in week 2 lectures 
- Storing data ?? dictionaries? One for users and one for channels 
- Created a file outlining the strucure 
- Named data_structure_plan.py in src folder 
    
Anto Questions/Feedback:
- Ignore the extra functions from the starter code -> just do the 9 in the table + clear 
- Make sure to use merge requests to make reviews and leave comments 
- Use the boards! 

# Secondary Meeting Notes (12-1pm)
- Assigned functions for everyone to work on using a spinning 
- Begun work on functions together 
- Test file name all end in _test, functions all start with test_ 

## MEETING TWO (WEEK THREE 03/03/2021)
# Description
Weekly meeting in lab/after lab
# Date
03/03/2021 - Lab + meeting (10-12, 12-1) 
# Attendees
Sesi, Kylee, Michael, Isabelle 
# Scribe
Isabelle 
# Lab Time Notes: 
- Merged our data storage variable into master 
- Adding assumptions regarding naming and allowed characters 
- Code review of clear function and tests (Michael??s code) 
- Code review of auth tests (Sesi??s code) 
- Decided on some extra tests to add and some minor style changes 

Antos Feedback: 
- Separate tests into as many as possible (ie one for valid name, one for invalid name etc) 
- Use fixtures to neaten code 
- Only test one thing in pytest raises so that everything gets caught 
- Name tests in a way that basically eliminates comments 


## MEETING THREE (WEEK THREE 07/03/2021)
# Description
Final Iteration One Meeting
# Date
07/03/2021 (10-12:30)
# Attendees
Isabelle, Kylee, Sesi, Michael
# Scribe
Isabelle 
# Agenda
- Assumptions file 
- Adding minutes to gitlab 
- Check return types 
- Permission_id? 
- Code review 
# Notes
- Make an assumptions txt file in the root directory 
    - Make one on each branch and list your assumptions then we will merge and resolve conflicts 
- Clear needs to be updated to reset lists rather than entire variable 
    - Changed and merged 
- Return types are in a dictionary 
- Change  global_owner_status to permission id: 
    - 1 is owner, 2 is not 
- Code review: 
    - Review when merging, maybe remain available to help edit? 
- Docstrings: 
    - Need them at the start of every function 
    - VSCode has auto docstrings 
- an AccessError is thrown when the auth_user_id passed in is not a valid id. 
- For next iterations: 
    - Write helper functions for checking user id and channel id exist 
- Did some pair coding to create some simple helper functions 
- Reviewed merge requests for auth together 
        