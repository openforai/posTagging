#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 24, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''
import sys
import time

import dataProcessing.ioOperation as iop
import dataProcessing.templateFileName as templateFileName
import taggers.baseLine.baseLineNp as baseLineNp


if __name__ == '__main__':    
    
    #print(sys.argv)
    
    base = sys.argv[1]
    bench = sys.argv[2]
    #print crossNum
    
    print("\nBase Line testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    tfn.builfResultFile('blm')
    
    start = time.time()
    
    words = iop.readWords(tfn.benchRandWords)
    pos = iop.readPos(tfn.benchRandCategories)
      
    meta = iop.readMetaData(tfn.benchRandMeta)
    maxLenPh = meta[1]
    #nbDistinctwords = meta[2]  
    #nbPos = meta[4]    
        
    blm = baseLineNp.BaseLineModel(words, pos)
    
    #blm.computeProb(tfn.benchRandTrainInd, maxLenPh)
    
    endInit = time.time()
    
    #blm.tagging(tfn.benchRandTest, tfn.benchRandResultTagging)
    
    end = time.time()
    
    print("\n\t- Initialization Time = {0}\n\t- Tagging Time = {1}\n\t- Total Time = {2}".format((endInit - start),(end - endInit), (end - start)))
    
    print "\n\nEnd of BLM Testing."
    