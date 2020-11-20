# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:22:40 2020

@author: Bosa
"""
import os
from emailManager import emailManager
from creditCardBillManager import creditCardBillManager
from dataAnalyzer import dataAnalyzer

if __name__ == "__main__":
    print("Testing running on shell")
    os.getcwd()
    newFolder = os.getcwd() + "\\Rechnungen"
    
    if os.path.exists(newFolder) != True:
        os.mkdir(newFolder)
    
    a = emailManager()
    print("Running creditCardBillManager")
    manager = creditCardBillManager(newFolder)
    
    print("Writing out the master data")
    manager.exportMasterToCSV()
    
    print("Writing out the monthly data")
    manager.exportMonthlyToCSV()
    
    plotter = dataAnalyzer(manager.generateMasterTable(), manager.generateMonthlyTable())
    #plotter.plotOverview()
    print(f"Overall sum is: {plotter.monthlyTable.NewAmount.sum()}")