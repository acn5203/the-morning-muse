import mysql.connector
import time
import smtplib


def send_email(Phone_email, msg):


    try:

        server = smtplib.SMTP('website', port)

        server.ehlo()

        server.starttls()

        server.login("email", "pwd")


        server.sendmail("email", Phone_email, msg)

        server.quit()

        print("Code ran successfully")

        return

    except:

        print("Email failed to send")




        return



t = time.localtime()


#Gets current time, looks at the hours only
current_time = time.strftime("%H", t)

print(current_time)


#Connects to database to fetch info
mydb = mysql.connector.connect(host="host", user="user", passwd="passws", database="db")



mycursor = mydb.cursor(buffered=True)


numberslst = []

timelst = []

carrierlst = []

id_lst = []



mycursor.execute("select * from users")



for i in mycursor:

    print("Entered loop")

    print(i)

    number = (str(i[2]))

    carrier = i[4]

    carrierlst.append(i[4])

    numberslst.append(str(number)+str(carrier))

    timelst.append(i[3])

    id_lst.append(i[0])







print("Done")




mycursor.execute("select * from allmessages")


website_link_present = False

link = ""

message_used = False

message = ""

message_id = ""


#FINDS THE MESSAGE NEEDED PORTION
#Checks first if the message has been used before, if it has continues to the next data row

for datarow in mycursor:


    message_id = datarow[0]

    used = datarow[3]

    #If message has been used, continue to next datarow

    if datarow[3] != None:

        continue

    #If this element is None, message has not been used yet, will continue operation

    if datarow[3] == None:

        message_used = False


        if datarow[2] != "":

            website_link_present = True

        elif datarow[2] == "":

            website_link_present = False


        #Sets up message as the quote
        message = datarow[1]


        #Sets up link as such if one is present
        if website_link_present == True:

            link = datarow[2]

        #Ends loop once a valid quote is found
        break


print("Message:", message)


#Loop through all names in DB and send message based on current time

for i in range(len(numberslst)):

    if current_time == "13" and timelst[i] == "est" and carrierlst[i] != "":

        print("Sending to:", numberslst[i])

        send_email(numberslst[i], message)

        time.sleep(30)

        if website_link_present == True:

            link_message = "If you want to check out the speech this was found, here is the link: {}".format(link)

            send_email(numberslst[i], link_message)


    if current_time == "14" and timelst[i] == "mt" and carrierlst[i] != "":

        print("Sending to:", numberslst[i])

        send_email(numberslst[i], message)

        if website_link_present == True:

            link_message = "If you want to check out the speech this was found, here is the link: {}".format(link)

            send_email(numberslst[i], link_message)




        print("Done sending messages for:", numberslst[i])




    if current_time == "15" and timelst[i] == "ct" and carrierlst[i] != "":

        print("Sending to:", numberslst[i])

        send_email(numberslst[i], message)

        if website_link_present == True:

            link_message = "If you want to check out the speech this was found, here is the link: {}".format(link)

            send_email(numberslst[i], link_message)

        print("Done sending messages for:", numberslst[i])



    if current_time == "16" and timelst[i] == "pst" and carrierlst[i] != "":

        print("Sending to:", numberslst[i])

        send_email(numberslst[i], message)

        if website_link_present == True:

            link_message = "If you want to check out the speech this was found, here is the link: {}".format(link)

            send_email(numberslst[i], link_message)


        sql = "UPDATE allmessages SET used = 1 WHERE id = '{}'".format(message_id)

        mycursor.execute(sql)

        mydb.commit()

        print("Done sending messages for:", numberslst[i])




print("Done whole list")


