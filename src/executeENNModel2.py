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
import taggers.ennTaggerModel2.ennModelNpModel2 as ennModelNp


if __name__ == '__main__':    
    
    #print(sys.argv)
    
    base = sys.argv[1]
    bench = sys.argv[2]
    trainModelArg = sys.argv[3]
    batchTrainArg = sys.argv[4]
    
    if( trainModelArg.upper() == 'TRUE' ):
        trainModel = True
    else:
        trainModel = False
        
    if( batchTrainArg.upper() == 'TRUE' ):
        batchTraining = True
    else:
        batchTraining = False
    
    
    print("\nENN Model 2 Tagger testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    tfn.builfResultFile('enn2', batch = batchTraining)
    
    start = time.time()
    
    if( trainModel ):    
        
        print "\n\n Building new model ... \n"
        
        meta = iop.readMetaData(tfn.benchRandMeta)
        nbPhrase = meta[0]
        maxLenPh = meta[1]      
        nbWords = meta[3]  
        #nbPos = meta[4]        
    
        words = iop.readWords(tfn.benchRandWords)
        pos = iop.readPos(tfn.benchRandCategories)
          
        ennTagger = ennModelNp.ElasticNN(words, pos)
        
        ennTagger.computeInitialProb(tfn.benchRandTrainInd, maxLenPh)
        
        endInit = time.time()
        
        if batchTraining :
            print "\n\n Batch Training. \n"
            ennTagger.trainningBatch(tfn.benchRandTrainENNInd, tfn.benchRandValidENNInd, maxLenPh, nbPhrase)
        else:
            print "\n\n Sequential Training. \n"
            ennTagger.trainningSeq(tfn.benchRandTrainENNInd, tfn.benchRandValidENNInd, maxLenPh, nbPhrase)
        
        endTraining = time.time()
        
        # Saved model
        with open(tfn.ennModelRandTagging, 'wb') as ennf:
            ennfPickle = pickle.Pickler(ennf)
            ennfPickle.dump(ennTagger)
            
    else:
        
        #tfn.ennModelRandTagging = "/home/adiks/Workspaces/Memory-2013/posTaggers/data/brown-dummy/testResult/enn/models/ennModelRandTagging_64-2.pickle"
        
        print " Reading saved model at : ", tfn.ennModelRandTagging
                
        with open(tfn.ennModelRandTagging, 'rb') as w:
            wPickle = pickle.Unpickler(w)
            ennTagger = wPickle.load()
        
        endInit = time.time()
        endTraining = time.time()
            
    ennTagger.tagging(tfn.benchRandTest, tfn.benchRandResultTagging)
    
    end = time.time()
        
    print("\n\t- Initialization Time = {0}\n\t- Training Time = {1}\n\t- Tagging Time = {2}\n\t- Total Time = {3}".format((endInit - start),(endTraining - endInit), (end - endTraining), (end - start)))
    
    print "\n\nEnd of ENN Tagger Testing."
    