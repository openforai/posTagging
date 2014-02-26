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
    maxCross = int(sys.argv[3])
    trainModel = True
    saved = False
    
    print("\nSecond Order HMM Tagger testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    
    for crossNum in range(1, maxCross+1):
        
        print "\n\n Second Order HMM Cross Testing " + str(crossNum)
        
        tfn.buildForCross(crossNum)
        tfn.builfResultFile('secHmm', crossNum)
        
        start = time.time()
        
        if( trainModel ): 
            words = iop.readWords(tfn.benchCrossWords)
            pos = iop.readPos(tfn.benchCrossCategories)
              
            meta = iop.readMetaData(tfn.benchCrossMeta)
            nbPhrase = meta[0]
            maxLenPh = meta[1]      
            nbWords = meta[3]  
            #nbPos = meta[4]
                
            secoHmmTagger = secoHmmModelNp.SecoHmmModel(words, pos)
            
            secoHmmTagger.computeInitialProb(tfn.benchCrossTrainInd, maxLenPh, nbPhrase, nbWords)
            
            # Saved model
            
            try:
             
                with open(tfn.secHmmModelCrossTagging, 'wb') as hmmf:
                    hmmfPickle = pickle.Pickler(hmmf)
                    hmmfPickle.dump(secoHmmTagger)
                    
                saved = True
                
            except MemoryError:
                saved = False
                print " Error When tried to saved model"
        else:
            
            print " Reading saved model at : ", tfn.secHmmModelCrossTagging
            
            with open(tfn.secHmmModelCrossTagging, 'rb') as w:
                wPickle = pickle.Unpickler(w)
                secoHmmTagger = wPickle.load()
                
            saved = True
        
        endInit = time.time()
        
        secoHmmTagger.tagging(tfn.benchCrossTest, tfn.benchCrossResultTagging)
        
        end = time.time()
        
        if not saved:
            print " Try to saved second time : "
            
            try:
             
                with open(tfn.secHmmModelCrossTagging, 'wb') as hmmf:
                    hmmfPickle = pickle.Pickler(hmmf)
                    hmmfPickle.dump(secoHmmTagger)
            except MemoryError:
                saved = False
                print " Error When tried to saved model"        
        
        
        print("\n\t- Initialization Time = {0}\n\t- Tagging Time = {1}\n\t- Total Time = {2}".format((endInit - start),(end - endInit), (end - start)))
    
    print "\n\nEnd of HMM Tagger Cross Testing."
    