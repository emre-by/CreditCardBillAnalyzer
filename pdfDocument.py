# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:38:20 2020

Pdf Document: Responsible for reading each bill (in pdf) and convert it to a
table (Pandas data frame). It takes out previous month's the paid amount.

@author: Bosa
"""
import re
import datetime
import PyPDF4
import pandas as pd
import numpy as np
#from time import perf_counter

class pdfDocument():
    '''
    Class for reading each bill and retrieving info
    '''

    def __init__(self, document):
        self.document = document
        *_, last = re.finditer(r'\\', document)
        self.filename = self.document[last.span()[1]:]

        ## Extract the raw data right at the initialization
        f = open(self.document, 'rb')
        pdf_reader = PyPDF4.PdfFileReader(f)
        npage = pdf_reader.getNumPages()
        page_text_all = ""

        for i in range(0, npage):
            page_text = pdf_reader.getPage(i)
            page_text_all += page_text.extractText()

        f.close()
        self.rawData = page_text_all

    @staticmethod
    def __midSearch__(keyword1, keyword2, source):
        k1 = re.search(keyword1, source)
        k2 = re.search(keyword2, source)

        try:
            a = source[k1.end() : k2.start()]
        except:
            print("Keyword(s) not found")
            a = '0'
        return a

    @staticmethod
    def __convertToFloat__(stringInput):
        temp = stringInput.replace('.', '')
        return float(temp.replace(',', '.'))

    @staticmethod
    def __convertToDate__(stringDate):
        return datetime.datetime.strptime(stringDate, '%d.%m.%Y')

    def __generateData__(self):
        # Cut the raw text between ALTER SALDO and NEUER SALDO
        cutBegin = "ALTER SALDO"
        cutEnd = "NEUER SALDO"
        datePattern = r'\d\d\W\d\d\W\d\d\d\d'
        sumPattern = r'\d\W\d\d'
        tableText = self.__midSearch__(cutBegin, (datePattern + '\n' + cutEnd), self.rawData)
        tableTextArray = np.array(re.split('\n', tableText))
        #tableTextArray = re.split('\n', tableText)

        # Retrieve the old sum
        date_iter = re.finditer(datePattern, tableText)
        a = next(date_iter)
        old_sum = re.sub('\n', '', tableText[0:a.start()])
        self.__old_sum__ = self.__convertToFloat__(old_sum)

        # Retrieve each item of the month's spendings
        # Remove the Einzahlung and date information at one index before,
        # and the amount one index after
        result = np.where(tableTextArray == 'EINZAHLUNG')

        if len(result[0]) != 0:
            index = result[0][0]
            indexArray = (tableTextArray == 'EINZAHLUNG')
            indexArray[index - 1] = True
            indexArray[index + 1] = True
            newArray = tableTextArray[np.invert(indexArray)]
            self.__old_paid__ = self.__convertToFloat__(tableTextArray[index + 1])
        else:
            self.__old_paid__ = 0
            newArray = tableTextArray

        table = []

        for i in range(0, len(newArray)):
            if re.search(datePattern, newArray[i]) != None:
                if (re.search(datePattern, newArray[i+3]) == None) & \
                    (re.search(sumPattern, newArray[i+3]) != None):
                    table.append([self.__convertToDate__(newArray[i]), \
                                newArray[i+1], newArray[i+2], \
                                self.__convertToFloat__(newArray[i+3])])
                else:
                    table.append([self.__convertToDate__(newArray[i]), \
                                  newArray[i+1], 'LocationNaN', \
                                  self.__convertToFloat__(newArray[i+2])])

        df = pd.DataFrame(data=table)
        df.columns = ['Date', 'Explanation', 'Location', 'Amount']

        self.__new_sum__ = df['Amount'].sum()
        self.__df__ = df

    def generateTable(self):
        self.__generateData__()
        return self.__df__

    def getNumberOfItems(self):
        self.__generateData__()
        return len(self.__df__)

    def getOldSum(self):
        self.__generateData__()
        return self.__old_sum__

    def getOldPaid(self):
        self.__generateData__()
        return self.__old_paid__

    def getNewSum(self):
        self.__generateData__()
        return self.__new_sum__

    def getAmountToPay(self):
        pattern1 = "NEUER SALDO"
        pattern2 = "Mindestbetrag"
        billSum = self.__midSearch__(pattern1, pattern2, self.rawData)
        billSum = self.__convertToFloat__(billSum)
        return billSum

    def getBillDate(self):
        keyw1 = "Rechnung_"
        keyw2 = "_40000155449"
        billDate = self.__midSearch__(keyw1, keyw2, self.filename)
        billDate = self.__convertToDate__(billDate)
        return billDate

    def checkSum(self):
        if self.getOldSum() + self.getOldPaid() + self.getNewSum() - self.getAmountToPay() < 0.1:
            cs = 1
        else:
            cs = 0
        return cs
