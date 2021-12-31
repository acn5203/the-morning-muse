

These Python scripts serve as the messaging system for the website

----------------------
carrier_lookup.py: pulls from website DB and looks up carrier of numbers using API. This also sends the welcome message if a valid carrier is found.
------------------------
Send-Morning-Messages.py: sends messages to all listed numbers on website DB at approx 8am for each timezone
------------------------
Read_Email.py: looks at responses to the website email (used to send  sms messages) and removes users from DB who respond  "STOP" and sends a message to user confirming removal from service.
------------------------