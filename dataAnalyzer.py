# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 16:13:57 2020

Data Analyzer: Responsible for creating plots or showing credit card data.
It can either give an overview of all the bills or year & month specific bill.

@author: Bosa
"""
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import mathOperations as mh

class dataAnalyzer(object):
    # Input types, either CSV files or Pandas DataFrames
    def __init__(self, masterTable, monthlyTable):
        
        if type(masterTable) == pd.core.frame.DataFrame:
            self.masterTable = masterTable
        else:
            self.masterTable = pd.read_csv(masterTable)
            self.masterTable.Date = [datetime.datetime.strptime(datex, '%Y-%m-%d') for datex in self.masterTable.Date]
            
        if type(monthlyTable) == pd.core.frame.DataFrame:
            self.monthlyTable = monthlyTable
        else:
            self.monthlyTable = pd.read_csv(monthlyTable)
            self.monthlyTable.Date = [datetime.datetime.strptime(datex, '%Y-%m-%d') for datex in self.monthlyTable.Date]
            
        self.__binList__ = list(range(0, int(self.masterTable.Amount.max()), 10))
        
    # Plots & functions based on MonthlyTable data       
    def plotOverviewYearly(self, givenYear = 0):
        
        self.monthlyTable['AmountPerItem'] = self.monthlyTable.apply(lambda row: (row.NewAmount / row.ItemNumber), axis = 1)
        k = (self.monthlyTable.Date.dt.year == givenYear)
        
        if givenYear == 0:
            fig, axarr = plt.subplots(3, 1, figsize=(12, 8))
            self.monthlyTable.plot(x = "Date", y = "NewAmount", ax = axarr[0], color ='red', grid = True, marker='.')
            self.monthlyTable.plot(x = "Date", y = "ItemNumber", ax = axarr[1], grid = True, marker='.')
            self.monthlyTable.plot(x = "Date", y = "AmountPerItem", ax = axarr[2], color ='green', grid = True, marker='.')
            
            fig2, axNew = plt.subplots(figsize=(12, 8))
            axNew.plot(self.monthlyTable.Date, self.monthlyTable.NewAmount, color ='red', marker='.')
            axNew.set_xlabel('Time', fontsize = 14)
            axNew.set_ylabel('Amount €', color = 'red', fontsize = 14)
            axNew.grid(True)
            
            ax2 = axNew.twinx()
            ax2.plot(self.monthlyTable.Date, self.monthlyTable.ItemNumber, color = 'blue', marker = '.')
            ax2.set_ylabel('Number of Items', color = 'blue', fontsize = 14)
            
        else:
            fig, axarr = plt.subplots(3, 1, figsize=(15, 8))
            self.monthlyTable[k].plot(x = "Date", y = "NewAmount", ax = axarr[0], color ='red', grid = True, marker='.')
            self.monthlyTable[k].plot(x = "Date", y = "ItemNumber", ax = axarr[1], grid = True, marker='.')
            self.monthlyTable[k].plot(x = "Date", y = "AmountPerItem", ax = axarr[2], color ='green', grid = True, marker='.')
            
            fig2, axNew = plt.subplots(figsize=(15, 8))
            axNew.plot(self.monthlyTable[k].Date, self.monthlyTable[k].NewAmount, color ='red', marker='.')
            axNew.set_xlabel('Time', fontsize = 14)
            axNew.set_ylabel('Amount €', color = 'red', fontsize = 14)
            axNew.grid(True)
            
            ax2 = axNew.twinx()
            ax2.plot(self.monthlyTable.Date[k], self.monthlyTable.ItemNumber[k], color = 'blue', marker = '.')
            ax2.set_ylabel('Number of Items', color = 'blue', fontsize = 14)
        
        return fig, fig2
    
    def retrieveDataFromMonthly(self, givenYear, givenMonth = 0):
        l1 = (self.monthlyTable.Date.dt.year == givenYear)
        l2 = (self.monthlyTable.Date.dt.month == givenMonth)
        
        if givenMonth == 0:
            return self.monthlyTable[l1]
        else:
            return self.monthlyTable[l1 & l2]
    
    # Plots & functions based on MasterTable data
    
    # This function returns the data from MasterTable for the given month
    # or year. MonthlyTable is rather inconsistent because the billing date is 
    # different than the month beginning and the bill comes one month later. 
    def retrieveDataFromMaster(self, givenYear, givenMonth = 0):
        k1 = (self.masterTable.Date.dt.year == givenYear)
        k2 = (self.masterTable.Date.dt.month == givenMonth)
                
        if givenMonth == 0:
            print(f"Sum of all items from given date: {self.masterTable[k1].Amount.sum()}")
            return self.masterTable[k1]
        else:
            print(f"Sum of all items from given date: {self.masterTable[k1 & k2].Amount.sum()}")
            return self.masterTable[k1 & k2]

    def plotGivenDate(self, givenYear, givenMonth = 0, case = "p"):    
        if type(case) != str:
            print("Case type is wrong, it should be a string, p or r")
            return
        elif case == 'p':
            k2 = (self.masterTable.Date.dt.year == givenYear)
            k3 = (self.masterTable.Date.dt.month == givenMonth)
        elif case == 'r':
            k2 = (self.masterTable.Date.dt.year >= givenYear)
            k3 = (self.masterTable.Date.dt.month >= givenMonth)
        else:
            print("Case type should be either p or r")
            return
            
        k1 = (self.masterTable.Amount > 0)
        #k2 = (self.masterTable.Date.dt.year == givenYear)
        #k3 = (self.masterTable.Date.dt.month == givenMonth)
        
        if givenMonth == 0:
            self.masterTable[k1 & k2].Amount.plot.hist(bins = 30, grid = True)
        else:
            self.masterTable[k1 & k2 & k3].Amount.plot.hist(bins = 30, grid = True)
            
    def plotByWeeks(self, givenYear = 0, givenMonth = 0):
        k1 = (self.masterTable.Amount > 0)
        k2 = (self.masterTable.Date.dt.year >= givenYear)
        k3 = (self.masterTable.Date.dt.month >= givenMonth)
        
        newDataFrame = mh.discretizeByWeeks(self.masterTable[k1 & k2 & k3], "Date", "Amount")
        newDataFrame.plot(x="Date", y="Amount", grid = True, marker='.')
    
    def plotByMonths(self, givenYear = 0, givenMonth = 0):
        k1 = (self.masterTable.Amount > 0)
        k2 = (self.masterTable.Date.dt.year >= givenYear)
        k3 = (self.masterTable.Date.dt.month >= givenMonth)
        
        newDataFrame = mh.discretizeByMonths(self.masterTable[k1 & k2 & k3], "Date", "Amount")
        newDataFrame.plot(x="Date", y="Amount", grid = True, marker='.')