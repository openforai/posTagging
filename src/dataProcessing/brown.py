#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 20, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

import re
import pickle

import posSet

class BrownProcessing(object):
    '''
    Deals with Brown benchmark I/O and processing
    '''


    def __init__(self, benchBrown, baseBrown):
        '''
        Constructor
        '''
        
        self.benchBrown = benchBrown
        self.baseBrown = baseBrown
        
    def readOnePhrase(self, filePath):
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
           
        
    def readDataPhraseByPhrase(self):
        """ Read all brown data block by block"""
        
        with open(self.benchBrown, 'r') as bch:
            
            bench = bch.readline()
            
            baseFile = self.baseBrown + bench + '/'
            
            while True:
                
                f = bch.readline()
                
                if not f:
                    break
                
                f = f.strip()
                
                if ( (f != '\n') and (f != '') ):
                    
                    filePath =  baseFile + f
                    filePath = filePath.replace("\n", "")
                    
                    print("\nProcessing of : " + filePath)
                    
                    for line in self.readOnePhrase(filePath):
                        
                        phrases = line.split('./.')
                        
                        if(len(phrases) > 2):
                            print len(phrases)
                            print phrases
                        yield line
    #                     for ph in phrases: 
    #                         
    #                         ph = ph.strip()
    #                         
    #                         if ph != '' and ph != '\n':                                  
    #                             yield ph + ' ./.'
    
            
    def brownInitialProcessing(self, tfn, nbData):
   
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
        
        ambigousWords = list()
        posFreq = dict()
        
        nbPhrases = 0
        nbWords = 0
        nbAmbWords = 0        
        nbErrors = 0
        
        maxPhLen = 0
        maxPh =''
        
        ex = r"^\d+((\.\d+)|(/\d+))?$" # to check numbers
        
        
        print("\n Brown Initial processing ...")
        
        with open(tfn.benchError, 'w') as berrors, open(tfn.benchTrain, 'w') as btagged:
                
            for line in self.readDataPhraseByPhrase():
            
                #print("\n\n\n " + line)
                
                taggedWords = line.split(" ")
                phrase = ""
                tmpMaxPhLen = 0
                wellTagged = True
                
                for tags in taggedWords:
                    
                    tags = tags.strip()
                    
                    if ( (tags != '\n') and (tags != '') ):
                    
                        temp = tags.split('/')                
                        
                        if( (len(temp) != 2) ):
                            
                            if (( (len(temp) == 3) and (re.search(ex, temp[0]+"/"+temp[1]) is None) ) or (len(temp) > 3) or ( temp[1] in posSet.dummy) ):                        
                            
                                berrors.write(tags)
                                berrors.write('\n')
                                berrors.write(line)                           
                                berrors.write('\n')
                                berrors.write('\n')                            
                                wellTagged = False
                                nbErrors +=1
                                
                                break
                            
                        tabpos = temp[1].split('-')
                        #temp2 = [temp[0], temp[1]]
                        
                        if( len(tabpos) > 1 ):
                            temp[1] = tabpos[0]
                            
                            if( temp[0] == '--' ):                            
                                temp[1] = '--'
                        
    #                     if( temp[1] in ['7', '2', '1'] ):
    #                         print tags
    #                         print temp
    #                         print tabpos
    #                         print line
                            
                        if( ( temp[1] == 'nil' ) or (temp[1] in posSet.mixture) ): # UNKNOW TAG
                            berrors.write(tags)
                            berrors.write('\n')
                            berrors.write(line)
                            berrors.write('\n')
                            berrors.write('\n')
                                
                            wellTagged = False
                            nbErrors +=1
                                
                            break
                        
                        if( posSet.alias.has_key(temp[1]) ):
                            temp[1] = posSet.alias.get( temp[1] )        
                                    
                        if temp[0] == '``' :
                            temp[0] = temp[1] = '\'\''
                         
                        tag = "/".join(temp)
                            
                        phrase = phrase + " " + tag
                
                
                if wellTagged :        
                    
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
                                    
                            if("fw" in temp[1]):
                                print tags
                                print phrase
                            
                            if( wordsDico.has_key( temp[0] ) ):
                                pos = wordsDico.get(temp[0])
                                
                                if temp[1] not in pos :
                                    pos.append(temp[1])
                                    wordsDico[temp[0]] = pos
                                    
                                    if( len(pos) == 2): # This will appear one time
                                        
                                        #if( (temp[0] not in ambigousWords) and (re.search(ex, str(temp[0])) is None) ):
                                            ambigousWords.append(temp[0])
                                            #print "ambiguous"
                                if( len(pos) >= 2 ):
                                    nbAmbWords += 1
                                    
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
                                
                            if( posFreq.has_key( temp[1] ) ):
                                freq = posDico.get(temp[1])
                                posFreq[temp[1]] = posFreq.get(temp[1]) + 1 
                                    
                                    #print("\t [UPDATED] " + temp[1] + " >>> ADDED " + temp[0] + "\n")
                            else:
                                
                                posFreq[temp[1]] = 1
                
                    #maxPhLen = tmpMaxPhLen > maxPhLen ? tmpMaxPhlen : maxPhLen
                    
                    if tmpMaxPhLen > maxPhLen :
                        maxPhLen = tmpMaxPhLen                    
                        
                    btagged.write(phrase)
                    btagged.write('\n')
                    btagged.write('\n')
                
                if( (nbPhrases % 1000) == 0):
                    print ("\n\t- {0} phrases already registered.\n".format(nbPhrases))
                    
                if nbPhrases == nbData:
                    print " \nMaximum data Saved.\n"
                    break
                    
        print ("\n\t- {0} phrases registered.\n".format(nbPhrases))
                                 
        # Write dictionary of words
        with open(tfn.benchWordsDico, 'wb') as bwdico:
            bwdicoPickle = pickle.Pickler(bwdico)
            bwdicoPickle.dump(wordsDico)
            
        # Write dictionary of pos
        with open(tfn.benchPosDico, 'wb') as bpdico:
            bpdicoPickle = pickle.Pickler(bpdico)
            bpdicoPickle.dump(posDico)
        
        # write categories
        with open(tfn.benchCategories, 'wb') as bcats:
            bcatsPickle = pickle.Pickler(bcats)
            bcatsPickle.dump(categories)
            #print categories
            
        # write categories
        with open(tfn.benchPosFreq, 'wb') as bcatsFreq:
            bcatsFreqPickle = pickle.Pickler(bcatsFreq)
            bcatsFreqPickle.dump(posFreq)
            #print posFreq
            
        # write words
        with open(tfn.benchWords, 'wb') as bwords:
            bwordsPickle = pickle.Pickler(bwords)
            bwordsPickle.dump(words)
            #print words
            
        # write ambiguous words
        with open(tfn.benchAmbiguousWords, 'wb') as bambWords:
            bambWordsPickle = pickle.Pickler(bambWords)
            bambWordsPickle.dump(ambigousWords)
            #print ambigousWords
        
        # write metadata        
        with open(tfn.benchMeta, 'w') as bmeta:
            phrase = "NbPhrases : "+ str(nbPhrases)
            phrase = phrase + "\nMaxLenPhrase : " + str(maxPhLen)
            phrase = phrase + "\nNbDistinctwords : " + str(len(words))            
            phrase = phrase + "\nNbWords : " + str(nbWords)
            phrase = phrase + "\nNbCategories : " + str(len(categories))
            phrase = phrase + "\nNbAmbiguousWords : " + str(nbAmbWords)
            phrase = phrase + "\nNbError : " + str(nbErrors)
            
            bmeta.write(phrase)
            
            
        
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
    
        print("\n Initial processing End.")
                
    
# End brownTrainWithMainCats