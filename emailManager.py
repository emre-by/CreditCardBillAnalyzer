# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 16:13:57 2020

Email Manager: Responsible for accessing email and looking for credit card bill
emails under "Finans/Faturalar" folder. It cross checks the latest email date
with the log file, i.e. if the bills from last months are already downloaded,
it is not going to re-download those.

@author: Bosa
"""
import os
import re
import email
import smtplib # Email access
import getpass # For hidden passwords
import imaplib
import datetime
#from time import perf_counter

class emailManager():

    def __init__(self):        
        self.status = {}
        self.__emailFolder__ = '"Finans/Faturalar"'
        self.__emailSubject__ = 'SUBJECT "Mastercard Gold - Rechnung"'

        self.__downloadFolder__ = os.getcwd() + "\\Rechnungen"
        if not os.path.exists(self.__downloadFolder__):
            os.mkdir(self.__downloadFolder__)
            self.__setResetTrigger__ = int(1)
        elif not os.listdir(self.__downloadFolder__):
            self.__setResetTrigger__ = int(1)
        else:
            self.__setResetTrigger__ = int(0)
        
        self.__checkLogFile__()       
        self.__login__()
        self.__findEmails__()
        self.__close__()    

    # Function to truncate datetime objects
    @staticmethod
    def __truncDatetime__(someDate):
        return someDate.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def __resetDate__(self):
        self.__logNumberOfBills__ = 1000
        self.__logLastBillDate__ = datetime.datetime(2050, 1, 1, 0, 0)

    def __checkLogFile__(self):
        print("Checking log file")
        try:
            if self.__setResetTrigger__ != int(1):
                logFileX = os.getcwd() + "\\creditCardBillManager.Log"
                logFile = open(logFileX, "r")
                lineArray = logFile.readlines()

                numberLine = str(lineArray[1])
                dateLine = str(lineArray[2])

                numberOfBills = numberLine.replace('Number of bills analyzed: ', '')
                numberOfBills = numberOfBills.replace('\n', '')
                self.__logNumberOfBills__ = int(numberOfBills)

                lastBillDate = dateLine.replace('Last bill date: ', '')
                lastBillDate = datetime.datetime.strptime(lastBillDate, '%Y-%m-%d %H:%M:%S')
                self.__logLastBillDate__ = self.__truncDatetime__(lastBillDate)
            else:
                self.__resetDate__()
        except:
            print("No log file found or data not consistent")
            self.__resetDate__()

    def __login__(self):
        ######## Accessing Email ########
        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_object.ehlo()
        smtp_object.starttls()

        self.__M__ = imaplib.IMAP4_SSL('imap.gmail.com')
        i = 0
        while i < 3:
            user = input("Enter your email: ")
            password = getpass.getpass("Enter your password: ")
           
            try:
                self.__M__.login(user, password)
                print("Logged into email server")
                break
            except:
                print("Wrong email or password!")
                i += 1
                
    def __findEmails__(self):
        ######## Finding Emails ########        
        print("Looking for emails")
        # a, b = self.__M__.list()
        self.__M__.select(self.__emailFolder__)
        _, data = self.__M__.search(None, self.__emailSubject__)

        ######## Convert Byte Array ########       
        newArray = data[0]
        x = newArray.decode("utf-8").split(' ')

        x_byte = []
        for item in x:
            x_byte.append(item.encode('utf-8'))
  
        ######## Get Email Dates ########        
        emailDateArray = []
        for item in x_byte:
            emailDateArray.append(self.__getEmailDate__(item))

        K = zip(emailDateArray, x_byte)
        Ksort = sorted(K, key=lambda t: t[0])

        self.__maxDate__ = Ksort[-1][0]
        self.__maxDateEMailId__ = Ksort[-1][1]
        self.__maxDate__ = self.__truncDatetime__(self.__maxDate__)

        ######## State Machine for the Cases ########
        if (self.__maxDate__ > self.__logLastBillDate__) \
            and ((len(x_byte) - 1) == self.__logNumberOfBills__):

            self.status[1] = 'UpdateLast'
            print("Last bill will be downloaded")
            self.__getEmailAttachment__(self.__maxDateEMailId__)
            print("Done")

        elif (self.__maxDate__ == self.__logLastBillDate__) \
            and (len(x_byte) == self.__logNumberOfBills__):

            self.status[0] = 'DoNothing'
            print("All the bills were already downloaded")
            print("Doing nothing")

        else:
            self.status[2] = 'GenerateAll'
            print("All the bills will be downloaded")
            for item in x_byte:
                self.__getEmailAttachment__(item)
            print("Done")
        
    def __getEmailDate__(self, email_id):
        result, email_data = self.__M__.fetch(email_id, "(RFC822)")   
        if result != 'OK':
            print("Error fetching email")
        else:
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            datePattern = r'\d\s\w\w\w\s\d\d\d\d'

            x = re.search(datePattern, raw_email_string)
            email_date = datetime.datetime.strptime(x.group(), '%d %b %Y')
                        
            return email_date

    def __getEmailAttachment__(self, email_id):
        ######## Download Attachments ########
        result, email_data = self.__M__.fetch(email_id, "(RFC822)")
        if result != 'OK':
            print("Error fetching email")
        else:
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            for part in email_message.walk():
                if part.get_content_type() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                    #body = part.get_payload(decode=True)
                    #print(body)

                filename = part.get_filename()
                att_path = os.path.join(self.__downloadFolder__, filename)

                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

    def __close__(self):
        ######## Close the server connection ########
        print("Closing the server connection")
        self.__M__.close()
        self.__M__.logout()
