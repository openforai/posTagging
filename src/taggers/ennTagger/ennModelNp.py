#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Nov 23, 2013

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''


import numpy as np
import re
from StringIO import StringIO

import emlp
import dataProcessing.ioOperation as iop

class ElasticNN(object):
    '''
     Elastic Neuro Tagger
    '''
    
    def __init__(self, words, posSet, l=3, r=3):
        
        print 'Initializing Elastic Neural Tagger ...'
        
        self.words = words
        self.posSet = posSet
        self.nbWords = len(self.words)
        self.nbPos = len(self.posSet)
        self.l = l
        self.r = r
        
        self.cwfreq = np.zeros((self.nbWords, self.nbPos))
        self.wfreq = np.zeros(self.nbWords)
        self.posfreq = np.zeros(self.nbPos)
        
        self.ew = np.zeros((self.nbWords, self.nbPos))
        
        self.eMlp = emlp.EMLP(self.nbPos, self.l, self.r)
        

    def buildInputAndTargetFromPhrase(self, inputs, targets, array, maxLenPh, newL, newR):
        '''
        Build Elastique Neuro Tagger Input from Indiced Phrased
        '''
        
        #print ph
        
        #inpt = np.zeros( (np.shape(ph)[0], (l+r+1)*self.nbPos ) )
        
        train = array[:maxLenPh]
        target = array[maxLenPh:]
        
        ph = train[(np.where(train > -1))] 
        
        
        k = 0
        #print np.shape(inputs)
        for i in range( np.shape(ph)[0] ):
            #print " I = " + str(i) + " \n"
            xi = (self.l - newL) * self.nbPos
            
            klr = i - newL
            
            while klr < 0 :
                xi += self.nbPos
                klr += 1
            #print " befor, XI = " + str(xi)
            while( (klr < np.shape(ph)[0]) and (klr <= (i + newR)) ):
                #print " klr = " + str(klr)
                for p in range(self.nbPos): 
                    #print "  XI = " + str(xi)                                                         
                    inputs[k, xi] = self.ew[ph[klr], p]
                    #print inputs[k, xi]
                    xi += 1
                    
                klr += 1                        
            
            k += 1
            
        tmpt = target[np.where(target > -1)] 
                    
        for i in range(np.shape(tmpt)[0]):
            targets[i][tmpt[i]] = 1
         
   
    def splitAndStrip(self, phrase):
        
        tokens = phrase.strip().split(" ")
        newT = list()
        for w in tokens :
            w = w.strip()
            if ( w != '') :
                #print " APPEND " + w
                newT.append( w )
        return newT
        
   
    def buildTestingInputFromPhrase(self, tokens, i, newL, newR):
        '''
        Build Elastique Neuro Tagger Input from Indiced Phrased
        '''
        
        inputs = np.zeros( (1, ((self.l+self.r+1)*self.nbPos) + 1 ) )
        inputs[:,np.shape(inputs)[1]-1:] = -1 # bias input
        
        k = 0
        
        #print " l, r = " + str(newL) + ", " + str(newR)
        
        
            #print " I = " + str(i) + " \n"
        xi = (self.l - newL) * self.nbPos
        
        klr = i - newL            
        
        while klr < 0 :
            xi += self.nbPos
            klr += 1
        #print " befor, XI = " + str(xi)
        while( (klr < len(tokens)) and (klr <= (i + newR)) ):
            #print " klr = " + str(klr)
            for p in range(self.nbPos): 
                
                tmphx = tokens[klr]
                
                ex = r"^\d+((\.\d+)|(/\d+))?$" # to check numbers

                if (re.search(ex, tmphx) is not None):            
                    tmphx = '0'
        
                if( tmphx in self.words ):
                    phi = self.words.index(tmphx)
                    #print tokens[klr] + " is Know"                                          
                    inputs[k, xi] = self.ew[phi, p]
                else:           # For Unknown Words
                    inputs[k, xi] = 1.0 / self.nbPos
                    #print tokens[klr] + " is UNKNOW"
                    
                xi += 1            
                 
            klr += 1                        
       
        return inputs
    
    
    
    def computeInitialProb(self, phrasesInd, length):
        '''
        Compute initial probability
        '''
        
        print "\nComputing different frequences ...\n"
        
        with open(phrasesInd, 'r') as f:
            
            ind = range(length)
            
            while True:
            
                data = f.readline()
                
                if not data:               
                    break
                
                array = np.genfromtxt(StringIO(data), dtype='int')
        
                for i in ind:
                    
                    #print(" {0} / {1}".format(array[i], array[i+length]))
                    if( array[i] > -1 ):
                        self.wfreq[ array[i] ] += 1
                        self.posfreq[ array[i+length] ] += 1
                        self.cwfreq[ array[i], array[i+length] ] +=1                    
                        
                #print self.cwfreq
                #print self.wfreq  
                
            for i in range(self.nbWords):            
                for j in range(self.nbPos):
                    self.ew[i,j] = ( self.cwfreq[i,j] ) / ( self.wfreq[i] )
                    
        #print self.ew  

    def validate(self, validInd, maxLenPh, posL, posR):
        
        inputs = np.zeros( (maxLenPh, ((self.l+self.r+1)*self.nbPos)+1) )   
        targets = np.zeros( (maxLenPh, self.nbPos ) )
        
        error = 0.0
        
        with open(validInd, "r") as vf:
            while True:
                    
                data = vf.readline()
                
                if not data:               
                    break
                
                array = np.genfromtxt(StringIO(data), dtype='int')
 
                
                inputs.fill(0.0)
                inputs[:,np.shape(inputs)[1]-1:] = -1 # bias input
                targets.fill(0.0)                    
                    
                self.buildInputAndTargetFromPhrase( inputs, targets, array, maxLenPh, posL, posR)
                
                outputs = self.eMlp.forward(inputs)
                
                error += 0.5 * np.sum( (targets-outputs) ** 2 )
                
        return error 
            
                    

    def trainning(self, phrasesInd, validInd, maxLenPh, nbPhrase):
        '''
        Train Elastic Neural Network
        '''
       
        print "Initialization of Training ..."
        
               
        inputs = np.zeros( (maxLenPh, ((self.l+self.r+1)*self.nbPos)+1) )   
        targets = np.zeros( (maxLenPh, self.nbPos ) )
        eta = 0.1
        
        old_val_error1 = 100002
        old_val_error2 = 100001
        new_val_error = 100000     
        
        shiftL = False
        posL = 1
        posR = 0
        
        with open(phrasesInd, 'r') as f:
            
            for size in range(1, self.r + self.l):
                    
                if shiftL :
                    posL += 1
                    shiftL = False
                else :
                    posR += 1
                    shiftL = True
                
                print " \n \tLearning for (l,r) = ({0},{1})".format(posL,posR)
                
                count = 0
                old_val_error1 = 100002
                old_val_error2 = 100001
                new_val_error = 100000     
        
                while (((old_val_error1 - new_val_error) > 0.001) or ((old_val_error2 - old_val_error1)>0.001)):
                    count+=1
                
                    f.seek(0,0) # move the pointer at the beginning
                    self.eMlp.updateLR(posL, posR) # Increase current l and r
                    
                    print " \n Lunching Iteration : ", count, " ..."
                        
                    while True:
                        
                        data = f.readline()
                        
                        if not data:               
                            break
                        
                        array = np.genfromtxt(StringIO(data), dtype='int')
                        
                        inputs.fill(0.0)
                        inputs[:,np.shape(inputs)[1]-1:] = -1 # bias input
                        targets.fill(0.0)                    
                        
                        self.buildInputAndTargetFromPhrase( inputs, targets, array, maxLenPh, posL, posR)
                       
                        #print inputs
                        #print targets
                        
                        #break
                        
                        self.eMlp.fwdBackwd(inputs, targets, eta)                    
                
                        #self.eMlp.weightUpdate() # used if self.eMlp.fwdBackwd2 is used above
                        
                        #break
                        
                    old_val_error2 = old_val_error1
                    old_val_error1 = new_val_error
                    
                    print "\n Lunching validation ..."
                    new_val_error = self.validate(validInd, maxLenPh, posL, posR)
                    
                    print " - (l,r) = ({0},{1}) : iter = {2}, error = {3}".format(posL, posR, count, new_val_error)




        
    def tagging(self, testingFile, res):
        '''
        Tagging one file
        '''
        
        print "\nTesting ...\n"
        
        with open(res, 'w') as rf:
            
            i = 0
            n = 1000
        
            for phrase in iop.getNextLine(testingFile):
                
                #print phrase
                
                if( np.mod(i, n) == 0):
                    print ("\n\t- {0} phrases already tagged.\n".format(i))
                                
                phraseRes = ""
                
                tokens = self.splitAndStrip(phrase)
                
                #print tokens
                
                for i in range(len(tokens)):
                    
                    tagged = False
                    
                    newL = self.l
                    newR = self.r
                    shiftL = False
                    
                    while( (not tagged) and ((newL+newR)>0)):
               
                        inputs= self.buildTestingInputFromPhrase(tokens, i, newL, newR)                
                    
                        out = self.eMlp.forward(inputs)
                        
                        tag = np.where(out == 1)
                    
                        #print tag
                        
                        if np.shape(tag[0])[0] == 1:
                            pos = self.posSet[tag[1][0]]
                       
                            phraseRes = phraseRes + " " + tokens[i] + "/" + pos
                            
                            tagged = True
                            
                            print tokens[i] + "/" + pos
                            
                        if shiftL :
                            newL -= 1
                            shiftL = False
                        else :
                            newR -= 1
                            shiftL = True
                            
                    if not tagged : # UNKNOWN TAG
                        phraseRes = phraseRes + " " + tokens[i] + "/" + "UnknownPOS"
                        
                phraseRes = phraseRes.strip()
               
                #print phraseRes    
                rf.write(phraseRes)
                rf.write("\n")
                
                i += 1
      
            print ("\n\t- {0} phrases tagged.\n".format(i))
            print "\nTesting End. Result saved in " + res
        
        
        
        