#! /usr/bin/python3

# Opens a csv of names and emails and randomly picks who you will buy a gift for
# Column order: ID,fname,lname,emailaddress

import random, csv
from exchangelib import Account, Credentials, Folder, Message, Mailbox

email_credentiasl_file = 'emailcredentials.csv'
exchange_user = ''
exchange_password = ''
exchange_email = ''
christmas_names_file = 'christmasnames.csv'
person_list = []
person_list_2 = []
selections = []

class Selection:
    def __init__(self,buyer,receiver):
        self.buyer = buyer
        self.receiver = receiver
    
    def __str__(self):
        #return "Test"
        return self.buyer.fname + " " + self.buyer.lname + " buys for " + self.receiver.fname + " " + self.receiver.lname
    
    def emailText(self):
        email_text = "Hi " + self.buyer.fname + "\r\n" + "You have drawn " + self.receiver.fname + " " + self.receiver.lname + " for a Christmas gift." "\r\n"
        email_text += "\r\nPlease keep your selection a secret, only make your selection known if you need help selecting a gift. The more people that you let know, the easier it is for people to guess."
        email_text += "\r\n"
        email_text += "Nobody reads emails sent here, if you have any questions you can ask Daniel."
        return email_text

class Person:
    def __init__(self, id, fname, lname, emailaddress):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.emailaddress = emailaddress
    
    def __str__(self):
        person_details = "ID: " + self.id + "\r\n"
        person_details += "Name: " + self.fname + " " + self.lname + "\r\n"
        person_details += "Email Address: " + self.emailaddress + "\r\n"
        return person_details

#This function sends emails
def sendEmailExhange(userName,password,fromEmail,toEmail,msgSubject,msgText):
    credentials = Credentials(userName,password)
    account = Account(fromEmail, credentials=credentials, autodiscover=True)
    m = Message(
        account=account,
        folder=account.sent,
        subject=msgSubject,
        body=msgText,
        to_recipients=[Mailbox(email_address=toEmail)]
    )
    m.send_and_save()
    print("Sent email to " + toEmail)

#This is the logic that runs the selection process and adds selections to the selections list
#Returns True if the selection process is successful, and False in the case where the last user draws themself
def makeSelections(person_list_1,person_list_2,selections):
    if not(len(person_list_1) == len(person_list_2)):
        print("Lists are different length somehow.")
    else:
        person_list_3 = person_list_2.copy()
        shuffle_count = 0
        for person in person_list_1:
            #Check for the last person selecting themselves and return false if that happens
            if(len(person_list_3)==1):
                if(person.id==person_list_3[0].id):
                    print("Last Selector Only Selected themself. Restarting Selecting Process.")
                    return False
            #Ensure this person has not been matched with themself. If they have, shuffle the second list.
            while (person.id == person_list_3[0].id):
                print(person.fname + " is the same as " + person_list_3[0].fname)
                print("Shuffling.")
                random.shuffle(person_list_3)
                shuffle_count += 1
                print(shuffle_count)
            #Add selections
            #Delete first row of person_list_2
            current_selection = Selection(person,person_list_3[0])
            selections.append(current_selection)
            del person_list_3[0]
        return True

###
# Load email credentials
###
with open(email_credentiasl_file) as email_credentials_csv:
    csv_reader = csv.reader(email_credentials_csv, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            line_count += 1
            if ''.join(row).strip():
                exchange_user = row[0]
                exchange_password = row[1]
                exchange_email = row[2]



###
# Load Data from CSV file and create person objects and place in person_list
###
with open(christmas_names_file) as christmas_names_csv:
    csv_reader = csv.reader(christmas_names_csv, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            line_count += 1
            if ''.join(row).strip():
                current_person = Person(row[0],row[1],row[2],row[3])
                person_list.append(current_person)

#duplicate person_list
person_list_2 = person_list.copy()

#run the make selections process
selecting_process_count = 0
selecting = False
while(selecting==False):
    selections = []
    selecting = makeSelections(person_list,person_list_2,selections)
    selecting_process_count += 1
    if(selecting_process_count > 10):
        selecting = True

summary_email = ""

for current_selection in selections:
    summary_email += str(current_selection)
    summary_email += "\r\n"
    sendEmailExhange(exchange_user,exchange_password,exchange_user,current_selection.buyer.emailaddress,"Christmas Gift Buying Selection",current_selection.emailText())

sendEmailExhange(exchange_user,exchange_password,exchange_user,exchange_user,"Christmas Gift Buying Selection Summary",summary_email)

exit()