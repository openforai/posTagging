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
import taggers.secoHmmTagger.secoHmmModelNp as secoHmmModelNp


if __name__ == '__main__':    
    
    #print(sys.argv)
    
    base = sys.argv[1]
    bench = sys.argv[2]
    trainModel = True
    
    
    print("\nSecond Order HMM Tagger testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    tfn.builfResultFile('secHmm')
    
    start = time.time()
    
    if( trainModel ): 
        
        words = iop.readWords(tfn.benchRandWords)
        pos = iop.readPos(tfn.benchRandCategories)
          
        meta = iop.readMetaData(tfn.benchRandMeta)
        nbPhrase = meta[0]
        maxLenPh = meta[1]      
        nbWords = meta[3]  
        #nbPos = meta[4]
        
        #print words
        #print pos
       
        secoHmmTagger = secoHmmModelNp.HmmModel(words, pos)
        
        secoHmmTagger.computeInitialProb(tfn.benchRandTrainInd, maxLenPh, nbPhrase, nbWords)
        
        # Saved model
        
        try:
                
            with open(tfn.secHmmModelRandTagging, 'wb') as hmmf:
                hmmfPickle = pickle.Pickler(hmmf)
                hmmfPickle.dump(secoHmmTagger)
        except MemoryError:
            print " Error When tried to saved model"
            
    else:
        
        print " Reading saved model at : ", tfn.secHmmModelRandTagging
        
        with open(tfn.secHmmModelRandTagging, 'rb') as w:
            wPickle = pickle.Unpickler(w)
            secoHmmTagger = wPickle.load()
    
    endInit = time.time()
    
    secoHmmTagger.tagging(tfn.benchRandTest, tfn.benchRandResultTagging)
    
    end = time.time()
    
    print("\n\t- Initialization Time = {0}\n\t- Tagging Time = {1}\n\t- Total Time = {2}".format((endInit - start),(end - endInit), (end - start)))
    
    print "\n\nEnd of Second Order HMM Tagger Testing."
    