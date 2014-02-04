#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 4, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

import numpy as np
from StringIO import StringIO
import re

import dataProcessing.ioOperation as iop

class BaseLineModel(object):
    '''
    Base Line model That used numpy lib
    '''


    def __init__(self, words, pos):
        '''
        Constructor
        
        '''
        self.words = words
        self.pos = pos
        
        self.nbPos = len(pos)
        self.nbWords = len(words)
        
        self.cwfreq = np.zeros((self.nbWords, self.nbPos))
        self.wfreq = np.zeros(self.nbWords)
        self.posfreq = np.zeros(self.nbPos)
        
        self.pcw = np.zeros((self.nbWords, self.nbPos))
        
        #print self.cwfreq
        #print self.wfreq
        
    def computeProb(self, phrasesInd, length):
        '''
        Compute initial probability
        '''
        
        print "\nComputing different frequences ...\n"
        
        with open(phrasesInd, 'r') as f:
        
            while True:
            
                data = f.readline()
                
                if not data:               
                    break
                
                array = np.genfromtxt(StringIO(data), dtype='int')
                #print array
                for i in range(length):                    
                    
                    #print(" {0} / {1}".format(array[i], array[i+length]))
                    if( array[i] > -1 ):
                        self.wfreq[ array[i] ] += 1
                        self.posfreq[ array[i+length] ] += 1
                        self.cwfreq[ array[i], array[i+length] ] +=1
                
                
        #print self.cwfreq
        #print self.wfreq  
        
        for i in range(self.nbWords):            
            for j in range(self.nbPos):
                self.pcw[i,j] = (self.cwfreq[i,j] + 1) / (self.wfreq[i] + self.nbPos)
                    
        #print self.pcw  
        
        
    def _computeWordTag(self, w):
        
        ex = r"^\d+((\.\d+)|(/\d+))?$" # to check numbers
        
        if (re.search(ex, w) is not None):            
            w = '0'
        
        if w in self.words :
            wInd = self.words.index(w)
            
            cInd = np.argmax(self.pcw[wInd])
            
        else :
            
            cInd = np.argmax(self.posfreq)
            
        return cInd
        
    def tagging(self, testingFile, resultFile):
        '''
        Tagging one file
        '''
        
        print "\nTesting ...\n"
        
        i = 0
        n = 1000
        
        with open(resultFile, 'w') as rf:
        
            for phrase in iop.getNextLine(testingFile):
                
                if( np.mod(i, n) == 0):
                    print ("\n\t- {0} phrases already tagged.\n".format(i))
                
                #print phrase
                
                words = phrase.strip().split(" ");
                phraseRes = ""
                
                for w in words :
                    
                    cInd = self._computeWordTag(w)
                    
                    pos = self.pos[cInd]
                    
                    phraseRes = phraseRes + " " + w + "/" + pos
                    phraseRes = phraseRes.strip()
                
                #print phraseRes    
                rf.write(phraseRes)
                rf.write("\n")
                
                i += 1
        
        print ("\n\t- {0} phrases tagged.\n".format(i))
        print "\nTesting End. Result saved in " + resultFile
                
                        
