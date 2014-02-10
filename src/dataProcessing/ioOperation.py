#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 21, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

import pickle
import numpy as np
import re

import posSet

def getNextLine(filePath):
    """ Read one line of phrase"""
   
    with open(filePath, 'r') as f:
            
        while True:
            
            newLine = f.readline()
            
            if not newLine:
                #print('END OF FILE')
                break
            
            else: 
                newLine = newLine.strip()
                        
                if( (newLine != '\n') and (newLine != '') ):                
                    yield newLine
                    

def getNextTestedLine(tested, truth):
    """ Read one line of phrase"""
   
    with open(tested, 'r') as testedFile,  open(truth, 'r') as truthfile:
        
        while True:
        
            boolTested = False
            boolTruth = False
            testedLine = ''
            truthLine = ''
                
            while not boolTested:
                
                testedLine = testedFile.readline()
                            
                if not testedLine:
                    #print('END OF FILE')
                    break
                
                else: 
                    testedLine = testedLine.strip()
                            
                    if( (testedLine != '\n') and (testedLine != '') ):                
                        boolTested = True
                        
            while boolTested and not boolTruth:
                
                truthLine = truthfile.readline()
                            
                if not truthLine:
                    #print('END OF FILE')
                    break
                
                else: 
                    truthLine = truthLine.strip()
                            
                    if( (truthLine != '\n') and (truthLine != '') ):                
                        boolTruth = True
                        
            if boolTested and boolTruth:
                yield (truthLine, testedLine)
            else:
                break
                    


def readDictionary(benchDico): 
    '''
    Read Benchmark dictionary from pickle format file
    '''
    
    global dictionary
    
    with open(benchDico, 'rb') as bdico:
        bdicoDePickle = pickle.Unpickler(bdico)
        dictionary = bdicoDePickle.load()
    
    #print("[BROWN DICTIONARY] : ", dictionary )
        

def readMetaData(benchMeta):
    '''
    Fetching meta data
    
    return an arrays of metada where
    meta[0] = nbPhrase
    meta[1] =  maxLenPhrase
    meta[2] =  nbDistinctwords
    meta[3] =  nbWords
    meta[4] = nbCategories
    meta[5] = NbAmbiguousWords
    meta[6] = nbError
    '''
    print 'Fetching Meta Data ...'
    
    meta = dict()
    
    with open(benchMeta, 'r') as bch:
            
            while True:
                data = bch.readline()
                
                if not data:            
                    break
                
                tmp = data.split(" ")
                meta[tmp[0]] = tmp[ len(tmp) -1 ].replace('\n', '')                
        
    #print(meta)
    
    nbPhrase = int(meta["NbPhrases"])
    maxLenPhrase = int(meta["MaxLenPhrase"])
    nbDistinctwords = int(meta["NbDistinctwords"])
    nbWords = int(meta["NbWords"])
    nbCategories = int(meta["NbCategories"])
    
    NbAmbiguousWords = 0
    
    if( "NbAmbiguousWords" in meta ):    
        NbAmbiguousWords = int(meta["NbAmbiguousWords"])
        
    nbError = int(meta["NbError"])
    
#         print("Number Of Phrases ", nbPhrase )
#         print("Max Length of Phrase ", maxLenPhrase)
#         print("Number Of Distinct words ", nbDistinctwords)
#         print("Number Of words ", nbWords)
#         print("Number Of Categories ", nbCategories)
#         print("Number Of Ambiguous Words ", NbAmbiguousWords)
#         print("Number Of Error Phrases ", nbError)
    
    return np.array([nbPhrase, maxLenPhrase, nbDistinctwords, nbWords, nbCategories, NbAmbiguousWords, nbError])


def readWords(wf):
    
    print "\nReading words ...\n"
    
    with open(wf, 'rb') as w:
        wPickle = pickle.Unpickler(w)
        words = wPickle.load()
    
    #print("[words] : ", words )
    
    return words


def readAmbiguousWords(awf):
    
    print "\nReading ambiguous words ...\n"
    
    with open(awf, 'rb') as w:
        wPickle = pickle.Unpickler(w)
        amwords = wPickle.load()
    
    #print("[words] : ", words )
    
    return amwords


def readPos(cf):
    
    print "\nReading POS ...\n"
    with open(cf, 'rb') as c:
        cPickle = pickle.Unpickler(c)
        categories = cPickle.load()
    
    #print("[categories] : ", categories )
    
    return categories

def readPosFreq(cf):
    
    print "\nReading POS Frequences ...\n"
    with open(cf, 'rb') as c:
        cPickle = pickle.Unpickler(c)
        posFreq = cPickle.load()
    
    #print("[categories] : ", categories )
    
    return posFreq


def readOnePhrase(filePath):
    """ Read one line of phrase of brown corpus """
   
    with open(filePath, 'r') as f:
        
        while True:
            
            newLine = f.readline()
            
            if not newLine:
                #print('END OF FILE')
                break
            
            else: 
                newLine = newLine.strip()
                        
                if( (newLine != '\n') and (newLine != '') ):                
                    yield newLine
           
        
def readDataPhraseByPhrase(listFile):
    """ Read all brown data block by block"""
    
    with open(listFile, 'r') as bch:
       
        while True:
            
            filePath = bch.readline()
            
            if not filePath:
                break
            
            filePath = filePath.strip()
            
            if ( (filePath != '\n') and (filePath != '') ):               
                
                filePath = filePath.replace("\n", "")
                
                print("\nProcessing of : " + filePath)
                
                for line in getNextLine(filePath):
                    
                    yield line

    
def translateIntoIndice(tagged, taggedInd, categories, words, nbPhrases, maxPhLen):
    
    print("\nTransforming data into indice ...\n")
            
    print("Nb Phrase ", nbPhrases )
    print("Max Length Phrase ", maxPhLen)
        
    ex = r"^\d+((\.\d+)|(/\d+))?$" # to check numbers
    
    nbCol = maxPhLen * 2 # words and tags
    
    data = np.ones((nbPhrases, nbCol), dtype='int') * -1
    
    ln = 0
       
    for phrase in getNextLine(tagged):
        phrase = phrase.strip()
        #print phrase
            
        taggedWords = phrase.split(" ")
        n = len(taggedWords)  
        col = 0
        
        for tags in taggedWords:
        
            tags = tags.strip()
                
            if ( (tags != '\n') and (tags != '') ):
                
                temp = tags.split('/')
                    
                #print ("temp {0}".format(temp))
                
                if (len(temp) == 3): # check fraction
                        
                    if (re.search(ex, temp[0]+"/"+temp[1]) is not None):
                        temp[0] = posSet.numberMarquee
                        temp[1] = temp[2]
                        temp[2] = ""
                    else:
                        print "CRITICAL ERROR"
                        exit()
                
                if (re.search(ex, temp[0]) is not None): # check number
                    temp[0] = posSet.numberMarquee
                
                iw = words.index(temp[0])
                ic = categories.index(temp[1])
                
                data[ln,col] = iw
                data[ln, nbCol/2 + col] = ic
                
                col += 1
        ln += 1
               
    #print data
    
    np.savetxt(taggedInd, data, '%-6d')
    print("\nIndiced Data saved in {0}".format(taggedInd))    