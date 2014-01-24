#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Oct 12, 2013

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

import numpy as np

class ForwardBackward:
    '''
     Compute the Forward-Backward procedure according to LAWRENCE R. RABINER paper : 
     A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition
    '''


    def __init__(self, hmm, oseq, alphaF=True, betaF=False):
        '''
        Constructor
        '''
        T = len(oseq)
        N = hmm.stateSize
        
        oseqInd = range( T )
        stateInd = range( N )
                
        self._alpha = np.zeros( (T, N) )
        self._beta = np.zeros( (T, N) )
        self._probability = 0.0
    
        def sumarizeAlphaStep(t, j) :
            '''
            Compute the probability of rich in state j at time t+1
            '''
            sumAlpha = 0.0
                    
            for i in stateInd :
                sumAlpha = sumAlpha + ( self._alpha[t, i] * hmm.getAij(i, j) ) 
        
            return sumAlpha;
            
        def computeAlpha():
            '''
            Compute the alpha arrays 
            '''
            
            # Initialization
            t = 0
            for i in stateInd :
                self._alpha[t, i] = hmm.getPii(i) * hmm.getBik(i, oseq[0])
            
            t += 1
            
            for o_t in oseqInd[1:] :
                o_t = oseq[t]    # observable at time t
            
                for j in stateInd :
                    self._alpha[t, j] = sumarizeAlphaStep(t-1, j) * hmm.getBik(j, o_t) 
            
                t += 1
                
        def sumarizeBetaStep(t, i) :
            '''
            The probability that the partial observables starting to time t if we are in state i at time t-1
            '''
            sumBeta = 0.0;
        
            o_t = oseq[t]    # observable at time t
        
            for j in stateInd :
                sumBeta = sumBeta + ( self._beta[t, j] * hmm.getBik(j, o_t) * hmm.getAij(i, j) ) 
        
            return sumBeta
        
        def computeBeta() :
            '''
            Compute the beta arrays
            '''
            
            # Initialization        
            
            t = T - 1;    # We start with the last observable
                    
            for i in stateInd :
                self._beta[t, i] = 1        
            
            for t in range(T-2, -1, -1) :
                
                for i in stateInd :
                    self._beta[t, i] = sumarizeBetaStep(t+1, i)
       
    
        def computeProbability() :
            '''
            Compute the last step of Forward or Backward procedure. <br/>
            If alphaF an betaF are both true, then only ALPHA flag will
            be considered
            '''
            prob = 0.0;
                        
            if alphaF : # Summarized the last alpha elements                
                for i in stateInd :
                    prob = prob + self._alpha[ T - 1, i]
                #print("ForWard") 
                    
        
            else :  #summarized the the first beta elements 
                # Probability that, if at time 0 we are in state i, we will observing the sequence o
                o_t = oseq[0] # observable at time 0
            
                for i in stateInd :
                    prob = prob + ( self._beta[0, i] * hmm.getPii(i) * hmm.getBik(i, o_t) )                    
                #print("Backward")
                
            self._probability = prob    
            
           
        if alphaF :
            computeAlpha()
        
        if betaF :
            computeBeta()
            
        computeProbability()

    def _getProbablilty(self):
        return self._probability
    
    def _setProbablilty(self):
        '''
        Never Modified it
        '''
        print('This probability is computed. You can''t updated it')
        
    def getAlphati(self, t, i) :
        return self._alpha[t, i]
            
    def getBetatj(self, t, j):
        return  self._beta[t, j]
    
    probability = property(_getProbablilty, _setProbablilty)  
    