#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Sept 2, 2013

@author: Paulin AMOUGOU
'''

import sys

import brown
import templateFileName
import ioOperation as iop

base = sys.argv[1]

bench = 'brown'
tfn = templateFileName.TemplateFileName(base, bench)

#tfn.buildFileName(base, bench)

bp = brown.BrownProcessing(tfn.benchFiles, tfn.baseBench) 

for ph in iop.readDataPhraseByPhrase(tfn.tmpBenchCross):
    #print ph
    pass