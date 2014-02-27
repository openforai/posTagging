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
import taggers.ennTagger.ennModelNp as ennModelNp


if __name__ == '__main__':    
    
    #print(sys.argv)
    
    base = sys.argv[1]
    bench = sys.argv[2]
    #maxCross = int(sys.argv[3])
    crossNum = int(sys.argv[3])
    trainModel = False
    batchTraining = True
    
    
    print("\nENN Tagger testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    
    #for crossNum in range(1, maxCross+1):
        
    print "\n\n ENN Line Cross Testing " + str(crossNum)
    
    tfn.buildForCross(crossNum)
    tfn.builfResultFile('enn', crossNum, batch = batchTraining)
    
    start = time.time()
    
    if( trainModel ): 
        words = iop.readWords(tfn.benchCrossWords)
        pos = iop.readPos(tfn.benchCrossCategories)
          
        meta = iop.readMetaData(tfn.benchCrossMeta)
        nbPhrase = meta[0]
        maxLenPh = meta[1]      
        nbWords = meta[3]  
        #nbPos = meta[4]
            
        ennTagger = ennModelNp.ElasticNN(words, pos)
        
        ennTagger.computeInitialProb(tfn.benchCrossTrainInd, maxLenPh)
        
        endInit = time.time()
        
        if batchTraining :
            ennTagger.trainningBatch(tfn.benchCrossTrainENNInd, tfn.benchCrossValidENNInd, maxLenPh, nbPhrase)
        else:
            ennTagger.trainningSeq(tfn.benchCrossTrainENNInd, tfn.benchCrossValidENNInd, maxLenPh, nbPhrase)
       
        endTraining = time.time()
        
        # Saved model
        with open(tfn.ennModelCrossTagging, 'wb') as ennf:
            ennfPickle = pickle.Pickler(ennf)
            ennfPickle.dump(ennTagger)
    else:
        
        print " Reading saved model at : ", tfn.ennModelCrossTagging
        
        with open(tfn.ennModelCrossTagging, 'rb') as w:
            wPickle = pickle.Unpickler(w)
            ennTagger = wPickle.load()
    
        endInit = time.time()
        endTraining = time.time()
    
    ennTagger.tagging(tfn.benchCrossTest, tfn.benchCrossResultTagging)
    
    end = time.time()
    
    print("\n\t- Initialization Time = {0}\n\t- Training Time = {1}\n\t- Tagging Time = {2}\n\t- Total Time = {3}".format((endInit - start),(endTraining - endInit), (end - endTraining), (end - start)))
    
    print "\n\nEnd of ENN Tagger Cross Testing."
    