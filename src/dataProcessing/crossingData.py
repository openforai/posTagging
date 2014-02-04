#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 22, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

from random import randrange
import re
import pickle
from math import ceil
import os

import ioOperation as iop
import posSet

class CrossingData(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def buildCrossDataFiles(self, tfn, maxCross):
        
        i = 1
        ci = 1
        generated = list()
        crossNum = dict()
        
        print(" Build {0} Cross Data Files ...".format(maxCross))
        
        meta = iop.readMetaData(tfn.benchMeta)
        
        #print(meta)
        
        nbPhrases = meta[0]
        
        print('\n Generating random line number ... \n')
         
        while i <= nbPhrases:
            tmpAlea = randrange(1, nbPhrases+1)
             
            if tmpAlea not in generated:
                
                if( crossNum.has_key(ci)):
                
                    nums = crossNum[ci]
                    nums.append(tmpAlea)
                    crossNum[ci] = nums                
                
                else:
                    nums = list()
                    nums.append(tmpAlea)
                    crossNum[ci] = nums
                    
                generated.append(tmpAlea)
                    
                #print("{0} generated".format(tmpAlea))
                i += 1
                ci += 1
                
                if ci > maxCross:
                    ci = 1
        
        ln = 1
        
        print " Splitting Data ...\n"
        
        for k in crossNum.keys(): # deleting file
            
            try:
                os.remove(tfn.benchCrossFiles.format(k))
                
            except OSError:
                pass
        
        for ph in iop.getNextLine(tfn.benchTrain):
            
            for k in crossNum.keys():
                if ln in crossNum.get(k):
                    with open(tfn.benchCrossFiles.format(k), 'a') as fcross:
                        fcross.write(ph)
                        fcross.write('\n')
                    ln += 1
                    break
                        
                        
        print " Crossing Data Generation ended.\n"



    def buildCrossBench(self, tfn, maxCross, crossNum):
        
            
        print " Building Crossing Bench File ..."
        
        with open(tfn.tmpBenchCross, 'w') as cross :
            #cross.write('data')
            for i in range(1, maxCross+1):            
                if( i != crossNum):                    
                    cross.write(tfn.benchCrossFiles.format(i))                    
                    cross.write('\n')
        

                    
    def buildCrossTrainAndMeta(self, tfn):
   
        '''
            This function build the new training data by removing extra pos
                e.g The/at-tl becomes The/at.
                
            It also builds the following features : 
            
                1- Dictionary : that contain each word with theirs categories
                2- Categories : that contain each distinct category
                3- Words      : that contain each distinct word
                3- MetaData   : that give information about bench set
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
        
        ex = r"^\d+((\.\d+)|(/\d+))?$" # to check numbers
        
        
        print("\n Cross Initial processing ...")
        
        with open(tfn.benchCrossError, 'w') as berrors, open(tfn.benchCrossTrain, 'w') as btagged:
                
            for phrase in iop.readDataPhraseByPhrase(tfn.tmpBenchCross):

                nbPhrases += 1
                tmpMaxPhLen = 0
                                
                phrase = phrase.strip()
                #print phrase
                
                taggedWords = phrase.split(" ")
                
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
                    
                btagged.write(phrase)
                btagged.write('\n')
                btagged.write('\n')
                    
                                 
        # Write dictionary of words
        with open(tfn.benchCrossWordsDico, 'wb') as bwdico:
            bwdicoPickle = pickle.Pickler(bwdico)
            bwdicoPickle.dump(wordsDico)
            
        # Write dictionary of pos
        with open(tfn.benchCrossPosDico, 'wb') as bpdico:
            bpdicoPickle = pickle.Pickler(bpdico)
            bpdicoPickle.dump(posDico)
        
        # write categories
        with open(tfn.benchCrossCategories, 'wb') as bcats:
            bcatsPickle = pickle.Pickler(bcats)
            bcatsPickle.dump(categories)
            #print categories
            
        # write words
        with open(tfn.benchCrossWords, 'wb') as bwords:
            bwordsPickle = pickle.Pickler(bwords)
            bwordsPickle.dump(words)
            #print words
        
        # write metadata        
        with open(tfn.benchCrossMeta, 'w') as bmeta:
            phrase = "NbPhrases : "+ str(nbPhrases)
            phrase = phrase + "\nMaxLenPhrase : " + str(maxPhLen)
            phrase = phrase + "\nNbDistinctwords : " + str(len(words))            
            phrase = phrase + "\nNbWords : " + str(nbWords)
            phrase = phrase + "\nNbCategories : " + str(len(categories))
            phrase = phrase + "\nNbError : " + str(nbErrors)
            
            bmeta.write(phrase)
            
        iop.translateIntoIndice(tfn.benchCrossTrain, tfn.benchCrossTrainInd, categories, words, nbPhrases, maxPhLen)    
        
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
    
        print("\n Cross processing End.")
                
    
# End brownTrainWithMainCats


    
    def buildCrossTestData(self, tfn, crossNum):
        
        print " Build Testing Data ... \n"
        
        ex = r"^\d+((\.\d+)|(/\d+))?$"
        
        with open(tfn.benchCrossTest, 'w') as btest, open(tfn.benchCrossTestParsed, 'w') as bparsed:
            
            for phrase in iop.getNextLine(tfn.benchCrossFiles.format(crossNum)):
                
                phrase = phrase.strip()
                #print phrase                  
                
                bparsed.write(phrase)
                bparsed.write('\n\n')
                
                tmpWt = phrase.split(' ')
                phNotParsed = "" 
                for wt in tmpWt:
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
                    
                        
    def buildCrossTestingFolder(self, tfn, maxCross):
        
        print(" Build {0} Testing Folder ...".format(maxCross))
        
        for num in range(1, maxCross+1):
            print " \n Crossing Folder :" + str(num) + "\n"
            tfn.buildForCross(num)
            self.buildCrossBench(tfn, maxCross, num)
            self.buildCrossTrainAndMeta(tfn)
            self.buildCrossTestData(tfn, num)
            
        print " End With Crossing Data Building."
        

    def splitValidationAndTrain(self, tfn, maxCross, percentage):
        
        print(" Build {0} Training and Validation data for ENN...".format(maxCross))
        
        for num in range(1, maxCross+1):
            print " \n Crossing Folder :" + str(num) + "\n"
            tfn.buildForCross(num)
            
            meta = iop.readMetaData(tfn.benchCrossMeta)
        
        #print(meta)
        
            nbPhrase = meta[0]
            nbValidPh =  int( ceil( nbPhrase * percentage / 100 ) )
            nbTrainPhrase = nbPhrase - nbValidPh
            
            print("Nb Phrase ", nbPhrase )
            print("Nb Train Phrase ", nbTrainPhrase)
            print("Nb Validation Phrase ", nbValidPh)
            
            i = 1
            aleaNum = list()
            
            print('\n Generating random line number ... \n')
            
            while i <= nbValidPh:
                tmpAlea = randrange(1, nbPhrase+1)
                
                if tmpAlea not in aleaNum:
                    aleaNum.append(tmpAlea)
                    i += 1
                    
            with open(tfn.benchCrossTrainENNInd, "w") as tennf, open(tfn.benchCrossValidENNInd, "w") as vldf:
                
                i = 1
                
                print( "\n Copying phrases ...")
                
                for ph in iop.getNextLine(tfn.benchCrossTrainInd):
                    
                    if i in aleaNum:
                        vldf.write(ph)
                        vldf.write('\n')                        
                    else:
                        tennf.write(ph)
                        tennf.write('\n')
                        
                    i += 1
                        
            
        
                