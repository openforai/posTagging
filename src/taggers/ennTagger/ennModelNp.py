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
import copy

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
                    #inputs[k, xi] = 1.0 / self.nbPos
                    inputs[k, xi] = self.posfreq[p] / np.sum(self.posfreq)
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
       
        error = 0.0
        
        with open(validInd, "r") as vf:
            while True:
                    
                data = vf.readline()
                
                if not data:               
                    break
                
                array = np.genfromtxt(StringIO(data), dtype='int') 
                
                nbW = np.shape(np.where(array>-1))[1] / 2
                inputs = np.zeros( (nbW, ((self.l+self.r+1)*self.nbPos)+1) )                   
                targets = np.zeros( (nbW, self.nbPos ) )
                
                inputs[:,np.shape(inputs)[1]-1:] = -1 # bias input
               
                self.buildInputAndTargetFromPhrase( inputs, targets, array, maxLenPh, posL, posR)
                
                outputs = self.eMlp.forward(inputs)
                
                error += 0.5 * np.sum( (targets-outputs) ** 2 )
                
        return error 
                                

    def trainningSeq(self, phrasesInd, validInd, maxLenPh, nbPhrase, niteration=5):
        '''
        Train Elastic Neural Network
        '''
       
        print "Initialization of Training ..."
 
        eta = 0.1
        
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
                
                self.eMlp.updateLR(posL, posR) # Increase current l and r
                
                count = 0
                old_val_error1 = 100002
                old_val_error2 = 100001
                new_val_error = 100000
                
                minError = new_val_error
                minModel = self.eMlp  
                minCount = 0      
        
                while (((old_val_error1 - new_val_error) > 0.001) or ((old_val_error2 - old_val_error1)>0.001)):
                    
                    self.eMlp.updateLR(posL, posR) # Here just the updated weight value will be fill to 0.0
                    
                    for tour in range(niteration):
                                                                    
                        count+=1
                    
                        f.seek(0,0) # move the pointer at the beginning
                        
                        
                        print " \n Lunching Iteration : ", count, " ..."
                            
                        while True:
                            
                            data = f.readline()
                            
                            if not data:               
                                break
                            
                            array = np.genfromtxt(StringIO(data), dtype='int')
                            nbW = np.shape(np.where(array>-1))[1] / 2
                            inputs = np.zeros( (nbW, ((self.l+self.r+1)*self.nbPos)+1) )   
                            targets = np.zeros( (nbW, self.nbPos ) )
                            change = range(nbW)
                                                        
                            inputs[:,np.shape(inputs)[1]-1:] = -1 # bias input
                                                       
                            self.buildInputAndTargetFromPhrase( inputs, targets, array, maxLenPh, posL, posR)
                           
                            np.random.shuffle(change)
                            inputs = inputs[change,:]
                            targets = targets[change,:]
                            
                            #print inputs
                            #print targets
                            
                            self.eMlp.fwdBackwd(inputs, targets, eta)                    
                    
                            # End Of Iteration
                            
                    old_val_error2 = old_val_error1
                    old_val_error1 = new_val_error
                    
                    print "\n validation ..."
                    new_val_error = self.validate(validInd, maxLenPh, posL, posR)
                    
                    print " - (l,r) = ({0},{1}) : iter = {2}, Validation Error = {3}, Training Error {4}: ".format(posL, posR, count, new_val_error, self.eMlp.error)

                    if new_val_error < minError :
                        minModel = copy.deepcopy(self.eMlp)
                        minError = new_val_error
                        minCount = count
                        print " - Minimal model set here."

                print "\n - Restoring model for last minimal error : ", minError
                self.eMlp = copy.deepcopy(minModel)
                new_val_error = self.validate(validInd, maxLenPh, posL, posR)
                print " - Validation (l,r) = ({0},{1}) : iter = {2}, Validation Error = {3}, Training Error {4}: ".format(posL, posR, minCount, new_val_error, self.eMlp.error)


    def trainningBatch(self, phrasesInd, validInd, maxLenPh, nbPhrase, niteration=5):
        '''
        Train Elastic Neural Network
        '''
       
        print "Initialization of Training ..."
        
        eta = 0.1
        
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
                
                self.eMlp.updateLR(posL, posR) # Increase current l and r
                
                count = 0
                old_val_error1 = 100002
                old_val_error2 = 100001
                new_val_error = 100000
                
                minError = new_val_error
                minModel = self.eMlp  
                minCount = 0   
        
                while (((old_val_error1 - new_val_error) > 0.001) or ((old_val_error2 - old_val_error1)>0.001)):
                    
                    self.eMlp.updateLR(posL, posR) # Here just the updated weight value will be fill to 0.0
                    
                    for tour in range(niteration):
                    
                        count+=1
                    
                        f.seek(0,0) # move the pointer at the beginning
                        
                        
                        print " \n Lunching Iteration : ", count, " ..."
                            
                        while True:
                            
                            data = f.readline()
                            
                            if not data:               
                                break
                            
                            array = np.genfromtxt(StringIO(data), dtype='int')
                            
                            nbW = np.shape(np.where(array>-1))[1] / 2
                            inputs = np.zeros( (nbW, ((self.l+self.r+1)*self.nbPos)+1) )   
                            targets = np.zeros( (nbW, self.nbPos ) )
                            change = range(nbW)
                            
                            inputs[:,np.shape(inputs)[1]-1:] = -1 # bias input
                            
                            self.buildInputAndTargetFromPhrase( inputs, targets, array, maxLenPh, posL, posR)
                           
                            np.random.shuffle(change)
                            inputs = inputs[change,:]
                            targets = targets[change,:]
                           
                            #print inputs
                            #print targets
                            
                            self.eMlp.fwdBackwdBatch(inputs, targets, eta)                    
                    
                        self.eMlp.weightUpdate() # used if self.eMlp.fwdBackwd2 is used above
                            
                            # End Of Iteration
                            
                    old_val_error2 = old_val_error1
                    old_val_error1 = new_val_error
                    
                    #print "\n Lunching  ..."
                    new_val_error = self.validate(validInd, maxLenPh, posL, posR)
                    
                    print " - Validation (l,r) = ({0},{1}) : iter = {2}, Validation Error = {3}, Training Error {4}: ".format(posL, posR, count, new_val_error, self.eMlp.error)
                    
                    if new_val_error < minError :
                        minModel = copy.deepcopy(self.eMlp)
                        minError = new_val_error
                        minCount = count
                        print " - Minimal model set here."
                        print " - Validation (l,r) = ({0},{1}) : iter = {2}, Validation Error = {3}, Training Error {4}: ".format(posL, posR, minCount, new_val_error, self.eMlp.error)
                    
                print "\n - Restoring model for last minimal error : ", minError
                self.eMlp = copy.deepcopy(minModel)
                new_val_error = self.validate(validInd, maxLenPh, posL, posR)
                print " - Validation (l,r) = ({0},{1}) : iter = {2}, Validation Error = {3}, Training Error {4}: ".format(posL, posR, minCount, new_val_error, self.eMlp.error)
            
        
    def tagging(self, testingFile, res):
        '''
        Tagging one file
        '''
        
        print "\nTesting ...\n"
        print "New Tagging method"
        
        with open(res, 'w') as rf:
            
            nbt = 0
            n = 1000
            mostTag = np.zeros(self.nbPos, dtype='int')
        
            for phrase in iop.getNextLine(testingFile):
                
                #print phrase
                
                if( np.mod(nbt, n) == 0):
                    print ("\n\t- {0} phrases already tagged.\n".format(nbt))
                                
                phraseRes = ""
                
                tokens = self.splitAndStrip(phrase)
                
                #print tokens
                
                for i in range(len(tokens)):
                    
                    tagged = False
                    
                    newL = self.l
                    newR = self.r
                    shiftL = False
                    
                    mostTag.fill(0)
                    
                    while( (not tagged) and ((newL+newR)>0)):
               
                        inputs= self.buildTestingInputFromPhrase(tokens, i, newL, newR)                
                    
                        out = self.eMlp.forward(inputs)
                        
                        tag = np.where(out >= 0.5)
                        mostTag[tag[1]] += 1
                        
                    
                        #print tag
                        
                        if np.shape(tag[0])[0] == 1:
                            pos = self.posSet[tag[1][0]]
                       
                            phraseRes = phraseRes + " " + tokens[i] + "/" + pos
                            
                            tagged = True
                            
                            #print tokens[i] + "/" + pos
                            
                        if shiftL :
                            newL -= 1
                            shiftL = False
                        else :
                            newR -= 1
                            shiftL = True
                            
                    if not tagged : # UNKNOWN TAG
                        
                        #print mostTag
                        
                        posi = np.argmax( mostTag )
                        
                        if( ((posi == 0) and (mostTag[0] > 0)) or (posi != 0) ):
                            pos = self.posSet[posi]
                       
                            phraseRes = phraseRes + " " + tokens[i] + "/" + pos
                            #print tokens[i] + "/" + pos
                            #print posi, mostTag[posi]
                        else:                       
                            
                            pos = self.posSet[ np.argmax(self.posfreq) ]
                            
                            phraseRes = phraseRes + " " + tokens[i] + "/" + pos
                        
                phraseRes = phraseRes.strip()
               
                #print phraseRes    
                rf.write(phraseRes)
                rf.write("\n")
                
                nbt += 1
      
            print ("\n\t- {0} phrases tagged.\n".format(nbt))
            print "\nTesting End. Result saved in " + res
        
        