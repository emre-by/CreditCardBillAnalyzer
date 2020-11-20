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
            
    def plotOverview(self, givenYear = 0):
        self.monthlyTable['AmountPerItem'] = self.monthlyTable.apply(lambda row: (row.NewAmount / row.ItemNumber), axis = 1)
        
        k = (self.monthlyTable.Date.dt.year == givenYear)
        
        if givenYear == 0:
            fig, axarr = plt.subplots(3, 1, figsize=(12, 8))
            self.monthlyTable.plot(x="Date", y="NewAmount", ax = axarr[0], color ='red')
            self.monthlyTable.plot(x="Date", y="ItemNumber", ax = axarr[1])
            self.monthlyTable.plot(x="Date", y="AmountPerItem", ax = axarr[2], color ='green')
        else:
            fig, axarr = plt.subplots(3, 1, figsize=(12, 8))
            self.monthlyTable[k].plot(x="Date", y="NewAmount", ax = axarr[0], color ='red')
            self.monthlyTable[k].plot(x="Date", y="ItemNumber", ax = axarr[1])
            self.monthlyTable[k].plot(x="Date", y="AmountPerItem", ax = axarr[2], color ='green')
        return fig
    
    def retrieveData(self, givenYear, givenMonth = 0):
        k1 = (self.masterTable.Date.dt.year == givenYear)
        k2 = (self.masterTable.Date.dt.month == givenMonth)
        
        l1 = (self.monthlyTable.Date.dt.year == givenYear)
        l2 = (self.monthlyTable.Date.dt.month == givenMonth)
        
        if givenMonth == 0:
            return self.masterTable[k1], self.monthlyTable[l1]
        else:
            return self.masterTable[k1 & k2], self.monthlyTable[l1 & l2]

    def plotGivenDate(self, givenYear, givenMonth = 0):
        k1 = (self.masterTable.Amount > 0)
        k2 = (self.masterTable.Date.dt.year == givenYear)
        k3 = (self.masterTable.Date.dt.month == givenMonth)
        
        if givenMonth == 0:
            self.masterTable[k1 & k2].Amount.plot.hist(bins = 30)
        else:
            self.masterTable[k1 & k2 & k3].Amount.plot.hist(bins = 30)
        
            
        
        
        
        