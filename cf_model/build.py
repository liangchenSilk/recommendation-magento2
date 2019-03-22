# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 22:56:50 2019

@author: Silk
"""

from data import Data
from gather_rawdata import GatherRawData
    
rawData = GatherRawData()
rawData.pickDataRange('2017-10-01', '2019-04-01')
data = Data()

trainY, trainR = data.getCountData()
trainX = data.getFeatureData()
#viewed = data.getViewedData()

print("TrainY: sizeX {}, sizeY {}".format(len(trainY), len(trainY[0])))
print("TrainR: sizeX {}, sizeY {}".format(len(trainR), len(trainR[0])))
print("TrainX: sizeX {}, sizeY {}".format(len(trainX), len(trainX[0])))
#print("Viewed: sizeX {}, sizeY {}".format(len(viewed), len(viewed[0])))

'''
write to txt file for ML training
'''
with open('trainY.txt', 'w') as file:
    for i in range(len(trainY)):
        for j in range(len(trainY[i])):
            file.write("%s\t" % trainY[i][j])
        file.write("\n")
        
with open('trainR.txt', 'w') as file:
    for i in range(len(trainR)):
        for j in range(len(trainR[i])):
            file.write("%s\t" % trainR[i][j])
        file.write("\n")
        
with open('trainX.txt', 'w') as file:
    for i in range(len(trainX)):
        for j in range(len(trainX[i])):
            file.write("%s\t" % trainX[i][j])
        file.write("\n")
'''      
with open('viewed.txt', 'w') as file:
    for i in range(len(viewed)):
        for j in range(len(viewed[i])):
            file.write("%s\t" % viewed[i][j])
        file.write("\n")
'''
