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
    trainModel = True
    
    
    print("\nBase Line testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    tfn.builfResultFile('blm')
    
    start = time.time()
    
    if trainModel :
    
        words = iop.readWords(tfn.benchRandWords)
        pos = iop.readPos(tfn.benchRandCategories)
          
        meta = iop.readMetaData(tfn.benchRandMeta)
        maxLenPh = meta[1]
        #nbDistinctwords = meta[2]  
        #nbPos = meta[4]    
            
        blmTagger = baseLineNp.BaseLineModel(words, pos)
        
        blmTagger.computeProb(tfn.benchRandTrainInd, maxLenPh)
        
        # Saved model
        with open(tfn.blmModelRandTagging, 'wb') as blmf:
            blmfPickle = pickle.Pickler(blmf)
            blmfPickle.dump(blmTagger)
    
    else:
        print " Reading saved model at : ", tfn.blmModelRandTagging
        
        with open(tfn.blmModelRandTagging, 'rb') as w:
            wPickle = pickle.Unpickler(w)
            blmTagger = wPickle.load()
    
    endInit = time.time()
    
    
    blmTagger.tagging(tfn.benchRandTest, tfn.benchRandResultTagging)
    
    end = time.time()
    
    print("\n\t- Initialization Time = {0}\n\t- Tagging Time = {1}\n\t- Total Time = {2}".format((endInit - start),(end - endInit), (end - start)))
    
    print "\n\nEnd of BLM Testing."
    