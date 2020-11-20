# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:12:31 2020

Credit Card Bill Manager: Responsible for retrieving tables (Pandas data frame)
of each credit card bill, pdfDocument objects, and generating the master & monthly
tables. Also, double  checks if the bills that are processed are fine, sum of 
individual costs match to the months' end -checksum. 

@author: Bosa
"""
import os
import re
import datetime
import pandas as pd
from pdfDocument import pdfDocument

class creditCardBillManager(object):
      
    def __init__(self, inputFolder):
        fileList = os.listdir(inputFolder)
        fullFileList = [(inputFolder + "\\" + x) for x in fileList]
        self.fileList = fullFileList
        
    def __generateLogFile__(self):
        pattern = r'\d\d\W\d\d\W\d\d\d\d'
        x = []
        for item in self.fileList:
            a = re.search(pattern, item)
            x.append(a.group(0))
        y = [datetime.datetime.strptime(datex, '%d.%m.%Y') for datex in x]
        
        logFile = open("creditCardBillManager.log", "w")
        logFile.write("Auto-generated report for the creditCardBillManager.py:\n")
        logFile.write("Number of bills analyzed: " + str(len(self.fileList)) + "\n")
        
        logFile.write("Last bill date: " + str(max(y)))
        logFile.close()
        
    def getLog(self):
        self.__generateLogFile__()
                    
    def checkSum(self):
        y = []
        k = iter(self.fileList)
        for item in k:
            x = pdfDocument(item)
            y.append(x.checkSum())
        
        if sum(y) == len(self.fileList):
            #print("Sanity check passed")
            return 1
        else:
            print("Sanity check failed, data frames and csv files will not be generated")
            return 0
            
            '''
            try:
                if x.checkSum() == 1:
                    print(f"{item} --OK--")
            except:
                print(f"{item} --ERROR--")
            '''
             
    def generateMasterTable(self):
        if self.checkSum() == 1:
            masterTableArray = []
            k = iter(self.fileList)
            for item in k:
                x = pdfDocument(item)
                masterTableArray.append(x.generateTable())
            self.__masterTable__ = pd.concat(masterTableArray)
            
            self.__generateLogFile__()
            return self.__masterTable__
        else:
            print("Error with the data")
            return 0
            
    def generateMonthlyTable(self):
        if self.checkSum() == 1:
            y= []
            k = iter(self.fileList)
            for item in k:
                x = pdfDocument(item)
                y.append([x.getBillDate(), x.getOldSum(), x.getOldPaid(), x.getAmountToPay(), x.getNumberOfItems()])
            
            self.__monthlyTable__ = pd.DataFrame(data = y)
            self.__monthlyTable__.columns = ['Date', 'OldSum', 'OldPaid', 'NewAmount', 'ItemNumber']
            
            self.__generateLogFile__()
            return self.__monthlyTable__
        else:
            print("Error with the data")
            return 0
        
    def exportMasterToCSV(self):
        self.generateMasterTable()
        self.__masterTable__.sort_values(by=['Date']).to_csv('MasterData.csv', index = False)
        
    def exportMonthlyToCSV(self):
        self.generateMonthlyTable()
        self.__monthlyTable__.sort_values(by=['Date']).to_csv('MonthlyData.csv', index = False)