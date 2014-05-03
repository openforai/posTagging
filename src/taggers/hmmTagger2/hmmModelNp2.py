#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Oct 9, 2013

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

import dataProcessing.ioOperation as iop

from hmmImpl2.hmm import HMM
from hmmImpl2.viterbi import Viterbi

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
        
        self.hmm = HMM(self.nbPos, self.nbObs + 1) # For Unknown Words
        
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
        
        uniTrans = np.zeros(self.nbPos)
        biTrans = np.zeros((self.nbPos, self.nbPos))
        
        uniDist = np.zeros((self.nbPos, self.nbObs))
        
        initFreq  = np.zeros(self.nbPos)
        
        with open(phrasesInd, 'r') as f:
        
            while True:
            
                data = f.readline()
                
                if not data:               
                    break
                
                array = np.genfromtxt(StringIO(data), dtype='int')
                
                nbph += 1
                
                i = 0
                initFreq[ array[i+length] ] += 1 # initial apparition
                uniTrans[ array[i+length] ]  += 1
                                
                uniDist[ array[i+length], array[i] ]  += 1
                
                for i in range(1, length):                    
                    
                    if( array[i] > -1 ):
                        
                        uniTrans[ array[i+length] ]  += 1
                        biTrans[ array[i+length-1], array[i+length] ]  += 1
                        
                        uniDist[ array[i+length], array[i] ]  += 1
                        

        if( nbph != nbPhrase):
            print "FATAL ERROR : DATA CORRUPTED, THE NUMBER OF PHRASES DID NOT MATCH"
            exit()
            
            
        C0 = int(np.sum(uniTrans))
                        
        for i in range(self.nbPos): 
            
            self.hmm.setPii(i, initFreq[i]/nbPhrase)
            
            #print "\n\n\n- pii(",i,") = \n", initFreq[i]/nbPhrase
            
            C1 = uniTrans[i]
            
            for j in range(self.nbPos):                
                
                N1 = uniTrans[j]
                N2 = biTrans[i,j]
                
                k2 = ( np.log10(N2 + 1) + 1) / ( (np.log10(N2+1)) + 2 )
                
                aij = k2*N2/C1 + (1-k2)*N1/C0
                
                self.hmm.setAij(i, j, aij)
                
            for k in range(self.nbObs):
                
                bik = uniDist[i,k] / uniTrans[i]
                
                self.hmm.setBik(i, k, bik)
                
            
            k = self.nbObs                
            bik = np.sum(uniDist[i]) / nbTobs  # For Unknown words
            self.hmm.setBik(i, k, bik)
        
        self.hmm.normalize()
        
        del initFreq
        
        del uniTrans
        del biTrans        
        
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
       
        bestPath = self.viterbi.computeBestPath(oseq)
        
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
        
        self.viterbi = Viterbi(self.hmm)
        
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
        