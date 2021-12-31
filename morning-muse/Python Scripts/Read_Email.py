



import email
import imaplib
import os
from imap_tools import MailBox, AND
import smtplib
import mysql.connector
from carrier_lookup import *


user = "user"
password = "passwd"
imap_url = "url"


attatchment_dir = 'dir'


def MailBox_Move():
    print("In move")
    with MailBox(imap_url).login(user, password, initial_folder='INBOX') as mailbox:
        print(mailbox.uids())
        for msg in mailbox.fetch():
            print(msg)

        uids = mailbox.uids()

        most_recent_uid = uids[-1]

        mailbox.move(most_recent_uid, 'INBOX.Flagged')


    return



def get_attatchments(msg):
    print("In attatchments function")
    filePath = attatchment_dir
    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join(attatchment_dir, fileName)
            with open(filePath, 'wb') as f:
                f.write(part.get_payload(decode=True))

        return filePath

    return None



mail = imaplib.IMAP4_SSL(imap_url)

mail.login(user, password)


mail.select("inbox")

most_recent = mail.select("inbox")[1][0]


#Reads most recent email (needs to extract attatchment)

#Checks if inbox is empty
if most_recent == b'0':
    print("No messages in inbox: EXIT") #No messages in inbox
    exit()



result, data = mail.fetch(most_recent,'(RFC822)')



raw = email.message_from_bytes(data[0][1])

new_attatchment_path = get_attatchments(raw)

contents = ""

#If there is an attatchment, extract text and read
if new_attatchment_path != None:
    with open(new_attatchment_path) as f:
        contents = f.read()
        contents = str(contents)


#If contents is stop/STOP, remove user from database/email/send confirmation
if (contents == "STOP") or (contents == "stop"):
    print("STOP found")

    sender = raw['From']




    sender_number = str(raw['From'])[:10]
    print(sender_number)

    mydb = mysql.connector.connect(host="host", user="user", passwd="pwd",
                               database="db")



    mycursor = mydb.cursor(buffered=True)

    sql = "DELETE from users WHERE number = '{}'".format(sender_number)

    mycursor.execute(sql)

    mydb.commit()

    print("Deleted user from table")


    mail.store(most_recent, "+FLAGS", "\\Deleted")
    mail.expunge()
    mail.close()
    mail.logout()

    send_email(sender, "You have been removed from our service list. Thank you for your time!")

else:
    print("moved to box")
    MailBox_Move() #Flags emails recieved that are not STOP
    send_email_self("An email has been flagged")


print("finished")

"""
if "Response" in message_string:

    print("Response found in message")

    print(message_string)


if "UNSTOP" in message_string:

    print("UNSTOP found")

if "STOP" in message_string:

    print("STOP found")
"""




