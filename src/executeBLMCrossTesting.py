#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 24, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''
import sys
import time
import pickle

import dataProcessing.ioOperation as iop
import dataProcessing.templateFileName as templateFileName
import taggers.baseLine.baseLineNp as baseLineNp


if __name__ == '__main__':    
    
    #print(sys.argv)
    
    base = sys.argv[1]
    bench = sys.argv[2]
    maxCross = int(sys.argv[3])
    #print crossNum
    
    print("\nBase Line testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    
    for crossNum in range(1, maxCross+1):
        
        print "\n\n Base Line Cross Testing " + str(crossNum)
        
        tfn.buildForCross(crossNum)
        tfn.builfResultFile('blm', crossNum)
        
        start = time.time()
        
        words = iop.readWords(tfn.benchCrossWords)
        pos = iop.readPos(tfn.benchCrossCategories)
          
        meta = iop.readMetaData(tfn.benchCrossMeta)
        maxLenPh = meta[1]
        #nbDistinctwords = meta[2]  
        #nbPos = meta[4]    
            
        blmTagger = baseLineNp.BaseLineModel(words, pos)
        
        blmTagger.computeProb(tfn.benchCrossTrainInd, maxLenPh)
        
        # Saved model
        with open(tfn.blmModelCrossTagging, 'wb') as blmf:
            blmfPickle = pickle.Pickler(blmf)
            blmfPickle.dump(blmTagger)
        
        endInit = time.time()
        
        blmTagger.tagging(tfn.benchCrossTest, tfn.benchCrossResultTagging)
        
        end = time.time()
        
        print("\n\t- Initialization Time = {0}\n\t- Tagging Time = {1}\n\t- Total Time = {2}".format((endInit - start),(end - endInit), (end - start)))
    
    print "\n\nEnd of BLM Cross Testing."
    