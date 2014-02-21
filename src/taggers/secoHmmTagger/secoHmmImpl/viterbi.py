#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Oct 5, 2013

@author: Paulin AMOUGOU
'''

import numpy as np

def viterbiProcessing(hmm, oseq):
    
    delta = np.zeros( (oseq.shape[0], hmm.stateSize, hmm.stateSize) )
    psy = np.zeros( (oseq.shape[0], hmm.stateSize, hmm.stateSize) )
        
    stateSequence = np.zeros( oseq.shape[0], dtype='int')
        
    oseqInd = range( len(oseq) )
    stateInd = range( hmm.stateSize )
    T = len(oseq)-1
    
    def _argMax(t, j, k):
        '''
        Compute arg max 
        Return a tuple (maxValue, argument)
        '''
         
        maxValue = 0.0
        arg = -1
        
        for i in stateInd:
            
            tmp = delta[t,i,j] * hmm.getAijk(i, j, k)
            
            if tmp > maxValue:
                maxValue = tmp
                arg = i
        
        return (arg, maxValue)
    
    def _recursionStep():
        '''
        Compute recursion step of Viterbi
        '''
        
        for t in oseqInd[1:]:   # Compute through observables.
            
            o_t = oseq[t]
            
            for j in stateInd:
                for k in stateInd:
                    
                    psy[t, j, k], delta[t, j, k] = _argMax(t-1, j, k)
                    
                    delta[t, j, k] = delta[t, j, k] * hmm.getBijk(j, k, o_t)
    
   

#   Initialization
     
    for i in stateInd:
        for j in stateInd:
        
            delta[0, i, j] = hmm.getPii(i) * hmm.getBijk(i, j, oseq[0]) # pi(i) * b_ij0
            psy[0, i, j] = 0

#    Recursion
    
    _recursionStep()

# Termination
    
    maxValue = 0.0
    argi = -1
    argj = -1
        
    for i in stateInd:
        for j in stateInd:
            
            if delta[T, i, j] > maxValue :
                maxValue = delta[T, i, j]
                argj = j
                argi = i
            
    stateSequence[T] = argj
    stateSequence[T-1] = argi
    probability = maxValue

    for t in sorted(oseqInd[:len(oseqInd)-2], reverse=True) :
        stateSequence[t] =  psy[t+1, stateSequence[t+1], stateSequence[t+2] ]
   
    return (stateSequence, probability) 