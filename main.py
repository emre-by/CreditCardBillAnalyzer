# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:22:40 2020

@author: Bosa
"""
import os
import datetime
from emailManager import emailManager
from creditCardBillManager import creditCardBillManager
from dataAnalyzer import dataAnalyzer

if __name__ == "__main__":
    print("Updating Credit Card Bills")
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
    plotter.plotOverviewYearly()
    print(f"Overall sum is: {plotter.monthlyTable.NewAmount.sum():1.2f}")
    
    #Get today's date
    x = datetime.date.today()
    k1 = plotter.monthlyTable.Date.dt.year == x.year
    k2 = plotter.monthlyTable.Date.dt.month == x.month
    k3 = plotter.monthlyTable.Date.dt.month == (x.month - 1)
    
    if len(plotter.monthlyTable[k1 & k2].NewAmount) != 0:
        amount = plotter.monthlyTable.NewAmount[k1 & k2].values[0]
        print(f"Final Bill is: {amount}")
    else:
        amount = plotter.monthlyTable.NewAmount[k1 & k3].values[0]
        print(f"Final Bill is: {amount}")
          