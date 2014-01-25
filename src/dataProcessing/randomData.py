#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 21, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

from random import randrange
from math import ceil
import re
import pickle


import ioOperation as iop
import posSet


class RandomData(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def buildTrainAndTestData(self, tfn, percentage):
        '''
        Build the training data and test data from main source
        '''
        wordsDico = dict()
        posDico = dict()
       
        categories = list()
        words = list()
        words.append(posSet.numberMarquee) # represent all the numbers
        
        nbPhrases = 0
        nbWords = 0
        nbErrors = 0
        
        maxPhLen = 0
        maxPh =''
        
        print('\n Building random training and testing data ... \n')
        
        ex = r"^\d+((\.\d+)|(/\d+))?$" # to check numbers         
        
        meta = iop.readMetaData(tfn.benchMeta)
        
        #print(meta)
        
        nbPhrase = meta[0]
        nbTestPhrase =  int( ceil( nbPhrase * percentage / 100 ) )
        nbTrainPhrase = nbPhrase - nbTestPhrase
        
        print("Nb Phrase ", nbPhrase )
        print("Nb Train Phrase ", nbTrainPhrase)
        print("Nb Test Phrase ", nbTestPhrase)
        
        i = 1
        aleaNum = list()
        
        print('\n Generating random line number ... \n')
        
        while i <= nbTestPhrase:
            tmpAlea = randrange(1, nbPhrase+1)
            
            if tmpAlea not in aleaNum:
                aleaNum.append(tmpAlea)
                i += 1
                #print("Found the {0}th number : {1}.".format(i, tmpAlea))
                
        #print(aleaNum)
        
        print " Randomly Splitting Data ... \n"
        
        with open(tfn.benchRandTrain, 'w') as btrain, open(tfn.benchRandTest, 'w') as btest, open(tfn.benchRandTestParsed, 'w') as bparsed:
            
            i = 1
            
            for phrase in iop.getNextLine(tfn.benchTrain):
                
                phrase = phrase.strip()
                #print phrase                  
                
                if i in aleaNum:
                    bparsed.write(phrase)
                    bparsed.write('\n\n')
                    
                    tmpWt = phrase.split(' ')
                    phNotParsed = "" 
                    for wt in tmpWt:
                        w = wt.split('/')
                        w = wt.split('/')
                    
                        if (len(w) == 3):
                                
                            if (re.search(ex, w[0]+"/"+w[1]) is not None):
                                w[0] = w[0]+"/"+w[1] #Fraction
                                w[1] = w[2]
                                w[2] = ""
                            else:
                                print "CRITICAL ERROR"
                                exit()
                            
                        phNotParsed = phNotParsed + w[0] + ' '
                    
                    btest.write(phNotParsed.strip())
                    btest.write('\n\n')
                    
                                
                else:                    
                            
                    nbPhrases += 1
                    tmpMaxPhLen = 0
                                                
                    taggedWords = phrase.split(" ")
                    phNotParsed = ""
                    
                    for tags in taggedWords:
                    
                        tags = tags.strip()
                        
                        if ( (tags != '\n') and (tags != '') ):
                        
                            temp = tags.split('/')
                            nbWords += 1
                            tmpMaxPhLen += 1
                            #print ("temp {0}".format(temp))
                            if (len(temp) == 3):
                                
                                if (re.search(ex, temp[0]+"/"+temp[1]) is not None):
                                    temp[0] = temp[0]+"/"+temp[1] #Fraction
                                    temp[1] = temp[2]
                                    temp[2] = ""
                                else:
                                    print "CRITICAL ERROR"
                                    exit()
                           
                            if( temp[1] not in categories ):
                                categories.append(temp[1])
                                
                            if( temp[0] not in words ):
                                if re.search(ex, str(temp[0])) is not None:
                                    #print ("{0} is a Number".format(temp[0]))
                                    pass
                                else:
                                    words.append(temp[0])
                                                       
                            if( wordsDico.has_key( temp[0] ) ):
                                pos = wordsDico.get(temp[0])
                                
                                if temp[1] not in pos :
                                    pos.append(temp[1])
                                    wordsDico[temp[0]] = pos 
                                    
                                    #print("\t [UPDATED] " + temp[0] + " >>> ADDED " + temp[1] + "\n")
                            else:
                                
                                pos = list()
                                pos.append(temp[1])
                                wordsDico[temp[0]] = pos
                                
                            if( posDico.has_key( temp[1] ) ):
                                wordsTemp = posDico.get(temp[1])
                                
                                if temp[0] not in wordsTemp :
                                    wordsTemp.append(temp[0])
                                    posDico[temp[1]] = wordsTemp 
                                    
                                    #print("\t [UPDATED] " + temp[1] + " >>> ADDED " + temp[0] + "\n")
                            else:
                                
                                wordsTemp = list()
                                wordsTemp.append(temp[0])
                                posDico[temp[1]] = wordsTemp
                                #nbDistinctWords += 1
                                
                                #print("\t [NEW] " + temp[1] + " >>> ADDED " + temp[0] + "\n")             
                    
                    #maxPhLen = tmpMaxPhLen > maxPhLen ? tmpMaxPhlen : maxPhLen
                    
                    if tmpMaxPhLen > maxPhLen :
                        maxPhLen = tmpMaxPhLen  
                    
                    btrain.write(phrase)
                    btrain.write('\n\n')
                
                i += 1
              
            
                    # Write dictionary of words
        with open(tfn.benchRandWordsDico, 'wb') as bwdico:
            bwdicoPickle = pickle.Pickler(bwdico)
            bwdicoPickle.dump(wordsDico)
            
        # Write dictionary of pos
        with open(tfn.benchRandPosDico, 'wb') as bpdico:
            bpdicoPickle = pickle.Pickler(bpdico)
            bpdicoPickle.dump(posDico)
        
        # write categories
        with open(tfn.benchRandCategories, 'wb') as bcats:
            bcatsPickle = pickle.Pickler(bcats)
            bcatsPickle.dump(categories)
            #print categories
            
        # write words
        with open(tfn.benchRandWords, 'wb') as bwords:
            bwordsPickle = pickle.Pickler(bwords)
            bwordsPickle.dump(words)
            #print words
        
        # write metadata        
        with open(tfn.benchRandMeta, 'w') as bmeta:
            phrase = "NbPhrases : "+ str(nbPhrases)
            phrase = phrase + "\nMaxLenPhrase : " + str(maxPhLen)
            phrase = phrase + "\nNbDistinctwords : " + str(len(words))            
            phrase = phrase + "\nNbWords : " + str(nbWords)
            phrase = phrase + "\nNbCategories : " + str(len(categories))
            phrase = phrase + "\nNbError : " + str(nbErrors)
            
            bmeta.write(phrase)
            
        iop.translateIntoIndice(tfn.benchRandTrain, tfn.benchRandTrainInd, categories, words, nbPhrases, maxPhLen)    
        
    #     print("[{0} DICTIONARY] : {1}".format(bench, dico) )
    #     
    #     print("Nb Phrases : ", nbPhrases)
    #     print("Max Phrase length : ", maxPhLen)
    #     print("Nb Distinct words : ", len(dico.keys()))
        print("Nb Words : ", nbWords)
        print("Nb Categories : ", len(categories))
    #     print("Nb Phrases with error : ", nbErrors)
    #     print("Categories : ", categories)
    #     print("Words : ", words)
            
    # END OF buildTrainAndTest