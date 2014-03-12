#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Oct 5, 2013

@author: Paulin AMOUGOU
'''

import numpy as np

class Viterbi(object):
    '''
    classdocs
    '''


    def __init__(self, hmm):
        '''
        Constructor
        '''
        
        self.hmm = hmm

    def computeBestPath(self, oseq):
        
        delta = np.zeros( (oseq.shape[0], self.hmm.stateSize) )
        psy = np.zeros( (oseq.shape[0], self.hmm.stateSize) )
            
        stateSequence = np.zeros( oseq.shape[0], dtype=int)
            
        oseqInd = range( len(oseq) )
        stateInd = range( self.hmm.stateSize )
        T = len(oseq)-1
        
        def _argMax(t, j):
            '''
            Compute arg max 
            Return a tuple (maxValue, argument)
            '''
             
            maxValue = 0.0
            arg = -1
            
            for i in stateInd:
                
                tmp = delta[t,i] * self.hmm.getAij(i, j)
                
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
                    
                    psy[t, j], delta[t, j] = _argMax(t-1, j)
                    
                    delta[t, j] = delta[t, j] * self.hmm.getBik(j, o_t)
        
       
    
    #   Initialization
         
        for i in stateInd:
            
            delta[0, i] = self.hmm.getPii(i) * self.hmm.getBik(i, oseq[0]) # pi(i) * b_i0
            psy[0, i] = 0
    
    #    Recursion
        
        _recursionStep()
    
    # Termination
        
        maxValue = 0.0
        arg = -1   
            
        for i in stateInd:
                
            if delta[T, i] > maxValue :
                maxValue = delta[T, i]
                arg = i
                
        stateSequence[T] = arg
        probability = maxValue
    
        for t in sorted(oseqInd[:len(oseqInd)-1], reverse=True) :
            stateSequence[t] =  psy[t+1, stateSequence[t+1] ]
       
        return (stateSequence, probability) 