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
import numpy as np
from pdfDocument import pdfDocument

class creditCardBillManager():
    """
    Class for retriving data frames, monthly and master
    """
    def __init__(self, inputFolder):
        fileList = os.listdir(inputFolder)
        # Generating the big master data at initialization so that other
        # functions do not need to regenerate the same data
        self.fileList = [(inputFolder + "\\" + x) for x in fileList]
        self.__masterData__ = np.array([pdfDocument(item) for item in self.fileList])
        self.__masterTable__ = None
        self.__monthlyTable__ = None

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
        '''
        Sanity check for the data, if the check sum of all bills are equal
        to number of bills

        Check sum logic for a single bill is (from pdfDocument.py)
            OldSum + OldPaid + NewSum() - AmountToPay() ~= 0

        Returns
        -------
        cs : check sum, either 1 or 0

        '''
        y = [item.checkSum() for item in self.__masterData__]

        if sum(y) == len(self.fileList):
            #print("Sanity check passed")
            cs = 1
        else:
            print("Sanity check failed, data frames and csv files will not be generated")
            cs = 0
        return cs

    def generateMasterTable(self):
        '''
        Generates the master table data frame

        Returns
        -------
        Pandas Data frame

        '''
        if self.checkSum() == 1:
            masterTableArray = []
            for item in self.__masterData__:
                masterTableArray.append(item.generateTable())
            self.__masterTable__ = pd.concat(masterTableArray)

            self.__generateLogFile__()
            return self.__masterTable__
        else:
            print("Error with the data")
            return 0

    def generateMonthlyTable(self):
        '''
        Generates the monthly table data frame

        Returns
        -------
        Pandas Data frame

        '''
        if self.checkSum() == 0:
            print("Error with the data")
            return 0
        else:
            y = []
            for item in self.__masterData__:
                y.append([item.getBillDate(), item.getOldSum(), \
                          item.getOldPaid(), item.getAmountToPay(), item.getNumberOfItems()])

            self.__monthlyTable__ = pd.DataFrame(data=y)
            self.__monthlyTable__.columns = ['Date', 'OldSum', 'OldPaid', 'NewAmount', 'ItemNumber']

            self.__generateLogFile__()
            return self.__monthlyTable__

    def exportMasterToCSV(self):
        '''
        Writes out the master table dataframe

        Returns
        -------
        None.

        '''
        self.generateMasterTable()
        self.__masterTable__.sort_values(by=['Date']).to_csv('MasterData.csv', index=False)

    def exportMonthlyToCSV(self):
        '''
        Writes out the monthly table dataframe

        Returns
        -------
        None.

        '''
        self.generateMonthlyTable()
        self.__monthlyTable__.sort_values(by=['Date']).to_csv('MonthlyData.csv', index=False)
