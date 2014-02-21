#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Oct 9, 2013

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

from secoHmmImpl.secoHmm import SecoHMM
from secoHmmImpl.viterbi import viterbiProcessing

import dataProcessing.ioOperation as iop


import numpy as np
from StringIO import StringIO
import re


class HmmModel(object):
    '''
    classdocs
    '''


    def __init__(self, obsSet, posSet):
        '''
        Constructor
        '''
        self.obsSet = obsSet
        self.posSet = posSet
        
        self.nbPos = len(posSet)
        self.nbObs = len(obsSet)
        
        self.hmm = SecoHMM(self.nbPos, self.nbObs + 1) # For Unknown Words
        
        self.posFreq = np.zeros(self.nbPos)
        self.initFreq  = np.zeros(self.nbPos)
        self.transitFreq = np.zeros( (self.nbPos, self.nbPos) )
        self.distFreq = np.zeros( (self.nbPos, self.nbObs) )    
      
      
    def computeInitialProb(self, phrasesInd, length, nbPhrase, nbTobs):
        '''
        Compute initial probability
        '''
        
        print "\nComputing different frequences ...\n"
        nbph = 0
        with open(phrasesInd, 'r') as f:
        
            while True:
            
                data = f.readline()
                
                if not data:               
                    break
                
                array = np.genfromtxt(StringIO(data), dtype='int')
                
                nbph += 1
                
                i = 0
                self.initFreq[ array[i+length] ] += 1 # initial apparition
                self.posFreq[ array[i+length] ] += 1
                self.distFreq[ array[i+length], array[i] ]  += 1
                
                for i in range(1, length):                    
                    
                    if( array[i] > -1 ):
                        
                        self.posFreq[ array[i+length] ] += 1
                        
                        self.transitFreq[ array[i+length-1], array[i+length] ] += 1
                        self.distFreq[ array[i+length], array[i] ]  += 1

        if( nbph != nbPhrase):
            print "FATAL ERROR : DATA CORRUPTED, THE NUMBER OF PHRASES DID NOT MATCH"
            exit()
            
            
        for i in range(self.nbPos): 
            
            self.hmm.setPii( i, self.initFreq[i]/nbPhrase )
            
            for j in range(self.nbPos):
                self.hmm.setAij( i, j, self.transitFreq[i,j]/self.posFreq[i] )
                       
            for k in range(self.nbObs):
                self.hmm.setBik( i, k, self.distFreq[i, k]/self.posFreq[i] )
            
            k = self.nbObs
            
            self.hmm.setBik( i, k, np.sum(self.distFreq[i])/nbTobs ) # For Unknown words
                
        
    def buildObsFromPhrase(self, phrase):
        
        def _splitAndStrip(phrase):
        
            tokens = phrase.split(" ")
            newT = list()
            for w in tokens :
                w = w.strip()
                if ( w != '') :
                    newT.append( w )
            return newT
        
        tokens = _splitAndStrip(phrase)
        
        oseq = np.zeros( len(tokens), dtype=int)
        newT = np.zeros( len(tokens), dtype = '|S50' )
        
        i = 0
        for tok in tokens :
            
            tokTemp = tok
            
            ex = r"^\d+((\.\d+)|(/\d+))?$" # to check numbers
        
            if (re.search(ex, tok) is not None):            
                tokTemp = '0'
            
            if tokTemp in self.obsSet :
                oseq[i] = self.obsSet.index( tokTemp )
                newT[i] = tok 
                
            else :                
                oseq[i] = self.nbObs # Unknown Words
                newT[i] = tok
                
            i += 1
        
        return ( (oseq, newT) ) 
     
                
    def computeTags(self, phrase):
        
        oseq, tokens = self.buildObsFromPhrase(phrase)
       
        bestPath = viterbiProcessing(self.hmm, oseq)
        
        #print("Seq : {0}".format(oseq))
        #print("Best Path : {0}, p = {1}".format(bestPath[0], bestPath[1]))
    
        res = np.zeros( len(bestPath[0]), dtype = '|S60' )
        
        for i in range(len(bestPath[0])) :
            res[i] = tokens[i] + '/' + self.posSet[ bestPath[0][i] ]
   
        return res
    
                    
    def tagging(self, testingFile, res):
        '''
        Tagging one file
        '''
        
        print "\nTesting ...\n"
        
        i = 0
        n = 1000
        
        with open(res, 'w') as rf:
        
            for phrase in iop.getNextLine(testingFile):
                
                #print phrase
                
                if( np.mod(i, n) == 0):
                    print ("\n\t- {0} phrases already tagged.\n".format(i))
                
                path = self.computeTags(phrase)
                
                phraseRes = ''
                for tag in path :                        
                        phraseRes = phraseRes + ' ' + tag    
                
                #print phraseRes    
                rf.write(phraseRes)
                rf.write("\n")
                
                i += 1
        
        print ("\n\t- {0} phrases tagged.\n".format(i))
        print "\nTesting End. Result saved in " + res
        