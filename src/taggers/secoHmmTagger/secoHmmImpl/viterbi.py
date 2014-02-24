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
    
    def _argMax(t, j, k, s_i):
        '''
        Compute arg max 
        Return a tuple (maxValue, argument)
        '''
         
        maxValue = 0.0
        arg = -1
        
        for i in stateInd[s_i:]:
            
            tmp = delta[t,i,j] * hmm.getAijk(i, j, k)
            
            if tmp > maxValue:
                maxValue = tmp
                arg = i
        
        return (arg, maxValue)
    
    def _recursionStep():
        '''
        Compute recursion step of Viterbi
        '''
        
        s_i = 0
        for t in oseqInd[1:]:   # Compute through observables.
            
            o_t = oseq[t]
            
            for j in stateInd[1:]:
                for k in stateInd[1:]:
                    
                    psy[t, j, k], delta[t, j, k] = _argMax(t-1, j, k, s_i)
                    
                    delta[t, j, k] = delta[t, j, k] * hmm.getBijk(j, k, o_t)
            s_i = 1
             

#   Initialization, delta has been initialized to zeros
     
    for i in stateInd:
        #print hmm.getPii(i)
        delta[0, 0, i] = hmm.getPii(i) * hmm.getBijk(0, i, oseq[0]) # pi(i) * b_ij0
        psy[0, 0, i] = 0
        
    #print psy[0]
    #print delta[0]

#    Recursion
    
    _recursionStep()

# Termination
    
    maxValue = 0.0
    argi = -1
    argj = -1
        
    for i in stateInd:
        for j in stateInd[1:]:
            
            if delta[T, i, j] > maxValue :
                maxValue = delta[T, i, j]
                argj = j
                argi = i
    
    stateSequence[T-1] = argi        
    stateSequence[T] = argj
    
    #print stateSequence
    #print delta[T]
    
    probability = maxValue

    for t in sorted(oseqInd[:len(oseqInd)-2], reverse=True) :
        #print t
        #print psy[t]
        stateSequence[t] =  psy[t+2, stateSequence[t+1], stateSequence[t+2] ]
        #print stateSequence
   
    stateSequence -= 1
    
    if -1 in stateSequence:
        print stateSequence
    
    return (stateSequence, probability) 