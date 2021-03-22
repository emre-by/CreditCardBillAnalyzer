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
    NEW_FOLDER = os.getcwd() + "\\Rechnungen"

    if not os.path.exists(NEW_FOLDER):
        os.mkdir(NEW_FOLDER)

    A = emailManager()
    print("Running creditCardBillManager")
    MANAGER = creditCardBillManager(NEW_FOLDER)

    print("Writing out the master data")
    MANAGER.exportMasterToCSV()

    print("Writing out the monthly data")
    MANAGER.exportMonthlyToCSV()

    PLOTTER = dataAnalyzer(MANAGER.generateMasterTable(), MANAGER.generateMonthlyTable())
    PLOTTER.plotOverviewYearly()
    print(f"Overall sum is: {PLOTTER.monthlyTable.NewAmount.sum():1.2f}")

    #Get today's date
    DATE = datetime.date.today()
    FILTER1 = PLOTTER.monthlyTable.Date.dt.year == DATE.year
    FILTER2 = PLOTTER.monthlyTable.Date.dt.month == DATE.month
    FILTER3 = PLOTTER.monthlyTable.Date.dt.month == (DATE.month - 1)

    if len(PLOTTER.monthlyTable[FILTER1 & FILTER2].NewAmount) != 0:
        AMOUNT = PLOTTER.monthlyTable.NewAmount[FILTER1 & FILTER2].values[0]
        print(f"Final Bill is: {AMOUNT}")
    else:
        AMOUNT = PLOTTER.monthlyTable.NewAmount[FILTER1 & FILTER3].values[0]
        print(f"Final Bill is: {AMOUNT}")
          