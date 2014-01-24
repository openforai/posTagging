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
percentage =  int(sys.argv[3])
maxCross =  int(sys.argv[4])

tfn = templateFileName.TemplateFileName(base, bench)

print("The benchmark used is located at : ", tfn.baseBench)

bp = brown.BrownProcessing(tfn.benchFiles, tfn.baseBench) 

bp.brownInitialProcessing(tfn)


rd = randomData.RandomData()

rd.buildTrainAndTestData(tfn, percentage)


cd = crossingData.CrossingData()

cd.buildCrossDataFiles(tfn, maxCross)

cd.buildCrossTestingFolder(tfn, maxCross)

fin = time.time()

print("\n Process done in {0} sec.".format((fin-debut)))

print "\nTraining and Testing Data Generation Ended.."
