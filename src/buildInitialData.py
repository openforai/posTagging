#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 20, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

import sys
import time

import dataProcessing.brown as brown
import dataProcessing.templateFileName as templateFileName
import dataProcessing.randomData as randomData
import dataProcessing.crossingData as crossingData

debut = time.time()

base = sys.argv[1]
bench = sys.argv[2]
nbData = int(sys.argv[3])
percentage =  int(sys.argv[4])
validation =  int(sys.argv[5])
maxCross =  int(sys.argv[6])

tfn = templateFileName.TemplateFileName(base, bench)

print("The benchmark used is located at : ", tfn.baseBench)

print " Nb data to use : ", nbData
print " Test data percentage : ", percentage
print " Validation data percentage for ENN : ", validation
print " Nb cross folder : ", maxCross

bp = brown.BrownProcessing(tfn.benchFiles, tfn.baseBench) 

bp.brownInitialProcessing(tfn, nbData)


rd = randomData.RandomData()

rd.buildTrainAndTestData(tfn, percentage)

rd.splitValidationAndTrain(tfn, validation)


cd = crossingData.CrossingData()

cd.buildCrossDataFiles(tfn, maxCross)

cd.buildCrossTestingFolder(tfn, maxCross)

cd.splitValidationAndTrain(tfn, maxCross, validation)



fin = time.time()

print("\n Process done in {0} sec.".format((fin-debut)))

print "\nTraining and Testing Data Generation Ended.."
