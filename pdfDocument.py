# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:38:20 2020

Pdf Document: Responsible for reading each bill (in pdf) and convert it to a
table (Pandas data frame). It takes out previous month's the paid amount.

@author: Bosa
"""
import re
import PyPDF4
import datetime
import pandas as pd

class pdfDocument(object):
    
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
    
    def __midSearch__(self, keyword1, keyword2, source):
        k1 = re.search(keyword1, source)
        k2 = re.search(keyword2, source)
        
        try:
            a = source[k1.end() : k2.start()]
        except:  
            print("Keyword(s) not found")
            a = '0'
        return a    
    
    def __convertToFloat__(self, stringInput):
        temp = stringInput.replace('.', '')
        return float(temp.replace(',', '.'))
    
    def __convertToDate__(self, stringDate):
        return datetime.datetime.strptime(stringDate, '%d.%m.%Y')
 
    def __generateData__(self):
        # Cut the raw text between ALTER SALDO and NEUER SALDO
        cutBegin = "ALTER SALDO"
        cutEnd = "NEUER SALDO"
        datePattern = r'\d\d\W\d\d\W\d\d\d\d'
        sumPattern = r'\d\W\d\d'
        tableText = self.__midSearch__(cutBegin, (datePattern + '\n' + cutEnd), self.rawData)
        tableTextArray = re.split('\n', tableText)
        
        # Retrieve the old sum
        date_iter = re.finditer(datePattern, tableText)
        a = next(date_iter)
        old_sum = re.sub('\n', '', tableText[0:a.start()])
        self.__old_sum__ = self.__convertToFloat__(old_sum)
         
        # Retrieve each item of the month's spendings
        table = []
        for i in range(0, len(tableTextArray)):
            if re.search(datePattern, tableTextArray[i]) != None:
                if (re.search(datePattern, tableTextArray[i+3]) == None) & (re.search(sumPattern, tableTextArray[i+3]) != None):
                    table.append([self.__convertToDate__(tableTextArray[i]), tableTextArray[i+1], tableTextArray[i+2], self.__convertToFloat__(tableTextArray[i+3])])
                else:
                    table.append([self.__convertToDate__(tableTextArray[i]), tableTextArray[i+1], 'LocationNaN', self.__convertToFloat__(tableTextArray[i+2])])
        
        df = pd.DataFrame(data = table)
        df.columns = ['Date', 'Explanation', 'Location', 'Amount']        
        
        a = df[df['Explanation'].str.match('EINZAHLUNG')]
        if a.empty == True:
            self.__old_paid__ = 0.0
        else:
            self.__old_paid__ = pd.to_numeric(a.iloc[0]['Amount'], downcast = 'float')
            df.drop(a.index, inplace=True)
        
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
        if (self.getOldSum() + self.getOldPaid() + self.getNewSum() - self.getAmountToPay() < 0.1):
            return 1
        else:
            return 0

        
        
        
        