# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 16:13:58 2018

@author: TUYEN
"""
import os
import numpy as np

class BNName:
    def __init__(self):
        self.BNType = None
        self.Side = None
        self.SensorType = None
        self.Fitness = None
        self.Trial = None
        self.BNIndex = None
    def __eq__(self, other):
        return self.BNType == other.BNType and \
                self.Side == other.Side and \
                self.SensorType == other.SensorType and \
                self.Fitness == other.Fitness and \
                self.Trial == other.Trial and \
                self.BNIndex == other.BNIndex
        

def BNNameParts(inimgname):
    bnname = BNName()
    filename = os.path.splitext(inimgname)[0]        
    srchidx = filename.find('-')
    bnname.BNType = filename[0 : srchidx]
    
    filename = filename[srchidx+1 : len(filename)]        
    srchidx = filename.find('-')
    bnname.Side = filename[0 : srchidx]
    
    filename = filename[srchidx+1 : len(filename)]
    srchidx = filename.find('-')
    bnname.SensorType = filename[0 : srchidx]
    
    filename = filename[srchidx+1 : len(filename)]
    srchidx = filename.find('-')
    bnname.Fitness = filename[0 : srchidx]
    
    filename = filename[srchidx+1 : len(filename)]
    srchidx = filename.find('-')
    bnname.Trial = filename[0 : srchidx]
    
    bnname.BNIndex = filename[srchidx+1 : len(filename)]
    
    return bnname        


RstLst_PathName1 = input('Input testing result file 1: ')
RstLst_fo1 = open(RstLst_PathName1, 'r')
RstLst1 = np.loadtxt(RstLst_fo1,
                     delimiter='\t',
                     dtype = {'names': ('col1', 'col2', 'col3', 'col4'),
                     'formats': ('S128', 'S128', 'S128', 'S2')})
RstLst_fo1.close

RstLst_PathName2 = input('Input testing result file 2: ')
RstLst_fo2 = open(RstLst_PathName2, 'r')
RstLst2 = np.loadtxt(RstLst_fo2,
                     delimiter='\t',
                     dtype = {'names': ('col1', 'col2', 'col3', 'col4'),
                     'formats': ('S128', 'S128', 'S128', 'S2')})
RstLst_fo2.close

IRTNameList = np.concatenate((RstLst1['col1'],RstLst2['col1']))
VR1NameList = np.concatenate((RstLst1['col2'],RstLst2['col2']))
VR2NameList = np.concatenate((RstLst1['col3'],RstLst2['col3']))
PredictedValueList = np.concatenate((RstLst1['col4'],RstLst2['col4']))

isGrouped = np.zeros(IRTNameList.shape[0])
BN_cnt = 0;Tot_QE = 0;PredictedValue = list()

for i in range(IRTNameList.shape[0]-1):
    if isGrouped[i]:
        continue    
    PredictedValue.clear()
    refName = BNNameParts(IRTNameList[i].decode('UTF-8'))
    refName.Trial = None
    isGrouped[i] = True
    BN_cnt += 1
    PredictedValue.append(PredictedValueList[i].decode('UTF-8'))
    Trial_cnt = 1    
    for j in range(i+1,IRTNameList.shape[0]):
        if isGrouped[j]:
            continue
        matchName = BNNameParts(IRTNameList[j].decode('UTF-8'))
        matchName.Trial = None
        if refName == matchName:
            Trial_cnt += 1
            PredictedValue.append(PredictedValueList[j].decode('UTF-8'))
            isGrouped[j] = True
            
    PredictedValue = sorted(set(PredictedValue))
    BelongingStageNum = len(PredictedValue)
    Tot_QE += ((BelongingStageNum - 1)/Trial_cnt)    
    
AQE = Tot_QE/BN_cnt
print(AQE)


        
    
    
    