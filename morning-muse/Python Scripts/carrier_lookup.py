import time
import requests
import json
import mysql.connector
import smtplib

def send_email(recipient, msg):

    try:

        server = smtplib.SMTP('email', port)

        server.ehlo()

        server.starttls()

        server.login("email", "pwd")


        server.sendmail("email", recipient, msg)

        server.quit()

        print("Code ran successfully")

        return

    except:

        print("Email failed to send")



def find_carrier(PhoneNumber):
    url = "https://twilio-lookup.p.rapidapi.com/PhoneNumbers/carrier"

    querystring = {"phoneNumber": "{}".format(PhoneNumber)}

    headers = {
        'x-rapidapi-host': "twilio-lookup.p.rapidapi.com",
        'x-rapidapi-key': "KEY"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    global res

    res = json.loads(response.text)

    carrier = ""

    print(res["carrier"]["name"])

    if "AT&T" in res["carrier"]["name"]:

        print("ATT is carrier")

        carrier = "@mms.att.net"



    elif "Verizon" in res["carrier"]["name"]:
        print("Verizon is carrier")

        carrier = "@vzwpix.com"



    elif "Sprint" in res["carrier"]["name"]:

        print("Sprint is carrier")

        carrier = "@pm.sprint.com"



    elif "T-Mobile" or "TMobile" or "t-mobile" in res["carrier"]["name"]:

        print("T-Mobile is carrier")

        carrier = "@tmomail.net"


    elif "Xfinity" or "xfinity" in res["carrier"]["name"]:

        print("Xfinity is carrier")

        carrier = "@mypixmessages.com"




    elif "Virgin" or "virgin" in res["carrier"]["name"]:

        print("Virgin Mobile is carrier")

        carrier = "@vmpix.com"

    else:
        print("Not listed carrier")

        carrier = ""

    return carrier





mydb = mysql.connector.connect(host="host", user="user", passwd="passwd",
                               database="db")

mycursor = mydb.cursor(buffered=True)

id_lst = []
numberslst = []

carrier_lst = []

personal_messagelst = []

mycursor.execute("select * from users")

for i in mycursor:
    print(i)

    number = "1" + (str(i[2]))

    numberslst.append(str(number))

    id_lst.append(i[0])

    carrier_lst.append(i[4])

    personal_messagelst.append(i[7])

print("Numbers list:", numberslst)

print("id list:", id_lst)

print("Carrier_lst", carrier_lst)

for i in range(len(carrier_lst)):

    print("Entered loop")

    print(i)

    if carrier_lst[i] == "":

        print("Searching carrier for:", numberslst[i])

        carrier = find_carrier(numberslst[i])

        if (carrier != ""):
            sql = "UPDATE users SET carrier = '{}' WHERE id = '{}'".format(carrier, id_lst[i])

            mycursor.execute(sql)

            mydb.commit()

            number = numberslst[i][1:]
            recipient = str(number)+str(carrier)


            print("Made changes to database")

            welcome_message = "Welcome! You were signed up for Morning Muse, so you will recieve a daily dose of motivation every morining! Feel free to share this positivity with your friends at www.the-morning-muse.com. If you wish to unsubscribe, reply STOP\n\nThis message is from the person who signed you up:\n{}".format(personal_messagelst[i])



            example_message = "Learn from yestarday, live for today, hope for tomorrow. The important thing is not to stop questioning. \n -Albert Einstein".format()

            send_email(recipient, welcome_message)

            time.sleep(45)

            sql = "UPDATE users SET first_time = '1' WHERE id = '{}'".format(id_lst[i])

            mycursor.execute(sql)

            mydb.commit()

            print("Sent first message and updated database")

        else:
            print("Carrier not listed: No changes made to db")
            continue

    else:

        print("Carrier listed")

        pass

print("Done")






