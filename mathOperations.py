# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 11:46:38 2020

Math Helper: A collection of various mathematical operations as well as 
functions to resize/shape datasets, i.e. summing values per week.

@author: Bosa
"""
import datetime
import pandas as pd
import numpy as np
from collections import Counter

def discretizeByWeeks(inputDataFrame, dateColumn, valueColumn):
    newDataFrame = pd.DataFrame()
    dateList = []
    itemNoList = []
    valueList = []
    
    yearList= list(inputDataFrame[dateColumn].dt.year)
    yearSet = set(yearList)
    
    for item in yearSet:
        k = (inputDataFrame[dateColumn].dt.year == item)
        weekList = list(inputDataFrame[k].Date.dt.isocalendar().week)
        weekCounter = Counter(weekList)
        for weeks in weekCounter:
            if len(yearSet) == 1:
                dateList.append(str(weeks))
            else:
                dateList.append(str(item) + "_" + str(weeks))
            itemNoList.append(weekCounter[weeks])
            # valueList.append(inputDataFrame[inputDataFrame[k].Date.dt.strftime("%W") == str(weeks)][valueColumn].sum())
            valueList.append(inputDataFrame[inputDataFrame[k].Date.dt.isocalendar().week == weeks][valueColumn].sum())

    newDataFrame[dateColumn] = dateList
    newDataFrame['ItemNumber'] = itemNoList
    newDataFrame[valueColumn] = valueList
    
    return newDataFrame

def discretizeByMonths(inputDataFrame, dateColumn, valueColumn):
    newDataFrame = pd.DataFrame()
    dateList = []
    itemNoList = []
    valueList = []
    
    yearList= list(inputDataFrame[dateColumn].dt.year)
    yearSet = set(yearList)
    
    for years in yearSet:
        k1 = (inputDataFrame[dateColumn].dt.year == years)
        monthList = list(inputDataFrame[k1].Date.dt.month)
        monthCounter = Counter(monthList)
        for months in monthCounter:
            datetime1= datetime.datetime(years, months, 1, 0, 0, 0, 0)
            dateList.append(datetime1)
            itemNoList.append(monthCounter[months])
            
            k2 = (inputDataFrame[dateColumn].dt.month == months)
            valueList.append(inputDataFrame[k1 & k2][valueColumn].sum())

    newDataFrame[dateColumn] = dateList
    newDataFrame['ItemNumber'] = itemNoList
    newDataFrame[valueColumn] = valueList
    
    return newDataFrame

def gaussDist(inputArray):
    mu, sigma = 0, 1
    return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (inputArray - mu)**2 / (2 * sigma**2) )

def meanNormalization(inputArray):
    stDev = np.std(inputArray)
    avr = np.mean(inputArray)
    mNorm = ((inputArray - avr) / stDev)
    return mNorm
