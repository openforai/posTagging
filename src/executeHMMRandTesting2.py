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
import taggers.hmmTagger2.hmmModelNp2 as hmmModelNp2


if __name__ == '__main__':    
    
    #print(sys.argv)
    
    base = sys.argv[1]
    bench = sys.argv[2]
    trainModelArg = sys.argv[3]
    
    if( trainModelArg.upper() == 'TRUE' ):
        trainModel = True
    else:
        trainModel = False
    
    
    print("\nNEW HMM Tagger testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    tfn.builfResultFile('hmm2')
    
    start = time.time()
    
    if( trainModel ): 
        
        print "\n\n Building new model ... \n"
            
        words = iop.readWords(tfn.benchRandWords)
        pos = iop.readPos(tfn.benchRandCategories)
          
        meta = iop.readMetaData(tfn.benchRandMeta)
        nbPhrase = meta[0]
        maxLenPh = meta[1]      
        nbWords = meta[3]  
        #nbPos = meta[4]
       
        hmmTagger = hmmModelNp2.HmmModel(words, pos)
        
        hmmTagger.computeInitialProb(tfn.benchRandTrainInd, maxLenPh, nbPhrase, nbWords)
        
        # Saved model
        with open(tfn.hmmModelRandTagging, 'wb') as hmmf:
            hmmfPickle = pickle.Pickler(hmmf)
            hmmfPickle.dump(hmmTagger)
            
    else:
        
        print " Reading saved model at : ", tfn.hmmModelRandTagging
        
        with open(tfn.hmmModelRandTagging, 'rb') as w:
            wPickle = pickle.Unpickler(w)
            hmmTagger = wPickle.load()
    
    endInit = time.time()
    
    hmmTagger.tagging(tfn.benchRandTest, tfn.benchRandResultTagging)
    
    end = time.time()
    
    print("\n\t- Initialization Time = {0}\n\t- Tagging Time = {1}\n\t- Total Time = {2}".format((endInit - start),(end - endInit), (end - start)))
    
    print "\n\nEnd of HMM Tagger Testing."
    