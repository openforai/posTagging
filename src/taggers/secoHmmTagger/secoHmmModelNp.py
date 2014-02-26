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


class SecoHmmModel(object):
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
        
        self.secoHmm = SecoHMM(self.nbPos+1, self.nbObs + 1) # +1 For Unknown Words and dummy POS
        
        
    def computeInitialProb(self, phrasesInd, length, nbPhrase, nbTobs):
        '''
        Compute initial probability
        '''
        
        print "\nComputing different frequences ...\n"
        uniTrans = np.zeros(self.nbPos+1)
        biTrans = np.zeros((self.nbPos+1, self.nbPos+1))
        triTrans = np.zeros((self.nbPos+1, self.nbPos+1, self.nbPos+1))
        
        uniDist = np.zeros((self.nbPos+1, self.nbObs))
        biDist = np.zeros((self.nbPos+1, self.nbPos+1, self.nbObs))
        
        posFreq = np.zeros(self.nbPos+1)
        initFreq  = np.zeros(self.nbPos+1)
        
        nbph = 0
        with open(phrasesInd, 'r') as f:
        
            while True:
            
                data = f.readline()
                
                if not data:               
                    break
                
                array = np.genfromtxt(StringIO(data), dtype='int')
                
                nbph += 1
                
                i = 0
                initFreq[ array[i+length]+1 ] += 1 # initial apparition
                #posFreq[ array[i+length]+1 ] += 1
                uniDist[ array[i+length]+1, array[i] ]  += 1
                biDist[ 0, array[i+length]+1, array[i] ]  += 1
                
                uniTrans[ array[i+length]+1 ]  += 1
                biTrans[ 0, array[i+length]+1 ]  += 1
                triTrans[ 0, 0, array[i+length]+1 ]  += 1
                
                for i in range(1, length):                    
                    
                    if( array[i] > -1 ):
                        
                        #posFreq[ array[i+length]+1 ] += 1
                        
                        uniDist[ array[i+length]+1, array[i] ]  += 1
                        biDist[ array[i+length-1]+1, array[i+length]+1, array[i] ]  += 1
                        
                        uniTrans[ array[i+length]+1 ]  += 1
                        biTrans[ array[i+length-1]+1, array[i+length]+1 ]  += 1
                        
                        if i > 1 :
                            triTrans[ array[i+length-2]+1, array[i+length-1]+1, array[i+length]+1 ]  += 1
                        else:
                            triTrans[ 0, array[i+length-1]+1, array[i+length]+1 ]  += 1
          
            #print initFreq
            #print posFreq
            #print uniDist
            #print biDist
            
            #print uniTrans
            #print biTrans
            #print triTrans
                        
        if( nbph != nbPhrase):
            print "FATAL ERROR : DATA CORRUPTED, THE NUMBER OF PHRASES DID NOT MATCH"
            exit()
        
        print " \n Computing probabilities ... \n"
        
        C0 = int(np.sum(uniTrans))
                        
        for i in range(self.nbPos+1): 
            
            self.secoHmm.setPii( i, initFreq[i]/nbPhrase )
            
            #print "\n\n\n- pii(",i,") = \n", initFreq[i]/nbPhrase
            
            for j in range(1, self.nbPos+1):
                
                C1 = uniTrans[j]
                C2 = biTrans[i,j]
                
                if(C2 == 0): # If C2 = 0, N3 will also be 0 since ij is not there, then ijk will not be there
                    C2 = 1 
                    
                for k in range(1, self.nbPos+1):
                    
                    N1 = uniTrans[k]
                    N2 = biTrans[j,k]
                    N3 = triTrans[i,j,k]                    
                    
                    k2 = ( np.log10(N2 + 1) + 1) / ( (np.log10(N2+1)) + 2 )
                    k3 = ( np.log10(N3 + 1) + 1) / ( (np.log10(N3+1)) + 2 )
                    
                    p = k3*N3/C2 + (1-k3)*k2*N2/C1 + (1-k3)*(1-k2)*N1/C0
                    
                    #print "\t- Aijk({0},{1},{2}) = {3}".format(i, j, k, p)
                
                    self.secoHmm.setAijk( i, j, k, p )
                       
                for k in range(self.nbObs):
                    
                    N2 = uniDist[j,k]
                    N3 = biDist[i,j,k]
                    
                    k2 = 1.0 / ( (np.log10(N3+1)) + 2 )
                    k3 = ( np.log10(N3 + 1) + 1) / ( (np.log10(N3+1)) + 2 )
                    
                    p = k3*N3/C2 + k2*N2/C1
                    
                    #print "\t\t- Bijk({0},{1},{2}) = {3}".format(i, j, k, p)
                    
                    self.secoHmm.setBijk( i, j, k, p )
                
                k = self.nbObs # For Unknown words
            
                N2 = np.sum(uniDist[j]) / nbTobs
                N3 = np.sum(biDist[i,j]) / nbTobs
                    
                k2 = 1.0 / ( (np.log10(N3+1)) + 2 )
                k3 = ( np.log10(N3 + 1) + 1) / ( (np.log10(N3+1)) + 2 )
                    
                p = k3*N3/C2 + k2*N2/C1
                
                #print "\t\t- Bijk({0},{1},{2}) = {3}".format(i, j, k, p)
                    
                self.secoHmm.setBijk( i, j, k, p ) 
        
        print " \n Normalize probabilities ... \n\n"
        self.secoHmm.normalize()    
        #self.secoHmm.display() 
        
        del initFreq
        del posFreq
        del uniDist
        del biDist
        
        del uniTrans
        del biTrans
        del triTrans   
        
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
       
        bestPath = viterbiProcessing(self.secoHmm, oseq)
        
        #print("Seq : {0}".format(oseq))
        #print("Best Path : {0}, p = {1}".format(bestPath[0], bestPath[1]))
    
        res = np.zeros( len(bestPath[0]), dtype = '|S60' )
        #print bestPath[0]
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
        