#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Oct 22, 2013

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

import numpy as np
from forwardBackward import ForwardBackward
from hmm import HMM

class BaumWelch(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def learn(self, hmm, oseq, nbIter=1):
        '''
        Build the new model that increase the probability of observing the sequence o
        '''
        
        T = len(oseq)
        N = hmm.stateSize
        
        oseqInd = range( T )
        stateInd = range( N )
        #interInd = range( nbIter )
        
        xi = np.zeros((T-1, N, N)) # 3-D arrays : (T-1) * N * N
        gamma = np.zeros((T, N))
        sumXi = np.zeros((N, N))
        sumGamma = np.zeros(N)
        
        fwbw = ForwardBackward(hmm, oseq, True, True)
        
        def calculateXi() :
            '''
            Compute the xi arrays
            '''
                                                                               
            po = fwbw.probability
        
            for t in oseqInd[:T-1] : # last transition start at T-1 to T.
                                    # we have T-1 possible transitions 
                for i in stateInd :
                
                    for j in stateInd : # x[t][i][j] probability of being in state i at time t and in state j at time t+1
                        xi[t, i, j] = fwbw.getAlphati(t, i) *  hmm.getAij(i, j) * hmm.getBik(j, oseq[t]) * fwbw.getBetatj(t+1, j) / po
         
         
        def calculateGamma() :
            '''
            Compute the gamma array
            '''
        
            for t in oseqInd[:T-1] :                
                for i in stateInd :
                    for j in stateInd :
                        gamma[t, i] += xi[t, i, j] # The nb transition from i at time t
            
            t += 1
            
            for j in stateInd :    # t = T, probability that the last observable will be produce by State j
                for i in stateInd :
                    gamma[t][j] = xi[t-1][i][j];
          
          
        calculateXi()
        calculateGamma()
        
        for i in stateInd : # compute the number of transition from state i to state j        
            for j in stateInd :
                for t in oseqInd[:T-1] :
                    sumXi[i, j] += xi[t, i, j];
                    
        for i in stateInd : # compute the number of transition from state i               
            for t in oseqInd[:T-1] :
                sumGamma[i] += gamma[t, i];
        
        newHmm = HMM(hmm.stateSize, hmm.obsSize)
        
        for i in stateInd :
            newHmm.setPii( i,  gamma[1, i] )
            
            for j in stateInd :
                newHmm.setAij(i, j, sumXi[i, j] / sumGamma[i] );    # aij
            
            for k in range(newHmm.obsSize) : #compute bik
                
                sumGammaOk = 0.0;
                t = 0;
                
                for t in oseqInd : #compute the number of times ot is produced by state i
                    
                    ot = oseq[t]
                    
                    if ot == k :
                        sumGammaOk += gamma[t][i];
                        #System.out.println(" obs " + ot );
                    
                
                newHmm.setBik(i, k, sumGammaOk / ( sumGamma[i] + gamma[T-1][i] )  ) # we add the last
            
        return newHmm    
            