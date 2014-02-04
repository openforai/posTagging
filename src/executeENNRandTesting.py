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
    
    
    print("\nENN Tagger testing ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    tfn.builfResultFile('enn')
    
    start = time.time()
    
    words = iop.readWords(tfn.benchRandWords)
    pos = iop.readPos(tfn.benchRandCategories)
      
    meta = iop.readMetaData(tfn.benchRandMeta)
    nbPhrase = meta[0]
    maxLenPh = meta[1]      
    nbWords = meta[3]  
    #nbPos = meta[4]
        
    ennTagger = ennModelNp.ElasticNN(words, pos)
    
    ennTagger.computeInitialProb(tfn.benchRandTrainInd, maxLenPh)
    
    endInit = time.time()
    
    ennTagger.trainning(tfn.benchRandTrainENNInd, tfn.benchRandValidENNInd, maxLenPh, nbPhrase)
    
    endTraining = time.time()
    
    # Saved model
    with open(tfn.ennModelRandTagging, 'wb') as ennf:
        ennfPickle = pickle.Pickler(ennf)
        ennfPickle.dump(ennTagger)
    
    ennTagger.tagging(tfn.benchRandTest, tfn.benchRandResultTagging)
    
    end = time.time()
    
    print("\n\t- Initialization Time = {0}\n\t- Training Time = {1}\n\t- Tagging Time = {2}\n\t- Total Time = {3}".format((endInit - start),(endTraining - endInit), (end - endTraining), (end - start)))
    
    print "\n\nEnd of ENN Tagger Testing."
    