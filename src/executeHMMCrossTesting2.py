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
import taggers.hmmTagger2.hmmModelNp2 as hmmModelNp


if __name__ == '__main__':    
    
    #print(sys.argv)
    
    base = sys.argv[1]
    bench = sys.argv[2]
    maxCross = int(sys.argv[3])
    trainModelArg = sys.argv[4]
    
    if( trainModelArg.upper() == 'TRUE' ):
        trainModel = True
    else:
        trainModel = False
    
    
    print("\nNEW HMM Tagger testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    
    for crossNum in range(1, maxCross+1):
        
        print "\n\n HMM Line Cross Testing " + str(crossNum)
        
        tfn.buildForCross(crossNum)
        tfn.builfResultFile('hmm2', crossNum)
        
        start = time.time()
        
        if( trainModel ): 
            
            print "\n\n Building new model ... \n"
            
            words = iop.readWords(tfn.benchCrossWords)
            pos = iop.readPos(tfn.benchCrossCategories)
              
            meta = iop.readMetaData(tfn.benchCrossMeta)
            nbPhrase = meta[0]
            maxLenPh = meta[1]      
            nbWords = meta[3]  
            #nbPos = meta[4]
                
            hmmTagger = hmmModelNp.HmmModel(words, pos)
            
            hmmTagger.computeInitialProb(tfn.benchCrossTrainInd, maxLenPh, nbPhrase, nbWords)
            
            # Saved model
            with open(tfn.hmmModelCrossTagging, 'wb') as hmmf:
                hmmfPickle = pickle.Pickler(hmmf)
                hmmfPickle.dump(hmmTagger)
        else:
            
            print " Reading saved model at : ", tfn.hmmModelCrossTagging
            
            with open(tfn.hmmModelCrossTagging, 'rb') as w:
                wPickle = pickle.Unpickler(w)
                hmmTagger = wPickle.load()
        
        endInit = time.time()
        
        hmmTagger.tagging(tfn.benchCrossTest, tfn.benchCrossResultTagging)
        
        end = time.time()
        
        print("\n\t- Initialization Time = {0}\n\t- Tagging Time = {1}\n\t- Total Time = {2}".format((endInit - start),(end - endInit), (end - start)))
    
    print "\n\nEnd of HMM Tagger Cross Testing."
    