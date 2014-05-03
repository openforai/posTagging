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


    def __init__(self, hmm):
        '''
        Constructor
        '''
        
        self.hmm = hmm
        self.N = hmm.stateSize
        self.stateInd = range( self.N )
    
    def learn(self, oseq, nbIter=1):
        '''
        Build the new model that increase the probability of observing the sequence o
        '''
        
        T = len(oseq)
        #self.N = hmm.stateSize
        
        oseqInd = range( T )
        #self.stateInd = range( self.N )
        #interInd = range( nbIter )
        
        xi = np.zeros((T-1, self.N, self.N)) # 3-D arrays : (T-1) * self.N * self.N
        gamma = np.zeros((T, self.N))
        sumXi = np.zeros((self.N, self.N))
        sumGamma = np.zeros(self.N)
        
        fwbw = ForwardBackward(self.hmm, oseq, True, True)
        
        def calculateXi() :
            '''
            Compute the xi arrays
            '''
                                                                               
            po = fwbw.probability
        
            for t in oseqInd[:T-1] : # last transition start at T-1 to T.
                                    # we have T-1 possible transitions 
                for i in self.self.stateInd :
                
                    for j in self.stateInd : # x[t][i][j] probability of being in state i at time t and in state j at time t+1
                        xi[t, i, j] = fwbw.getAlphati(t, i) *  self.hmm.getAij(i, j) * self.hmm.getBik(j, oseq[t]) * fwbw.getBetatj(t+1, j) / po
         
         
        def calculateGamma() :
            '''
            Compute the gamma array
            '''
        
            for t in oseqInd[:T-1] :                
                for i in self.stateInd :
                    for j in self.stateInd :
                        gamma[t, i] += xi[t, i, j] # The nb transition from i at time t
            
            t += 1
            
            for j in self.stateInd :    # t = T, probability that the last observable will be produce by State j
                for i in self.stateInd :
                    gamma[t][j] = xi[t-1][i][j];
          
          
        calculateXi()
        calculateGamma()
        
        for i in self.stateInd : # compute the number of transition from state i to state j        
            for j in self.stateInd :
                for t in oseqInd[:T-1] :
                    sumXi[i, j] += xi[t, i, j];
                    
        for i in self.stateInd : # compute the number of transition from state i               
            for t in oseqInd[:T-1] :
                sumGamma[i] += gamma[t, i];
        
        newHmm = HMM(self.hmm.stateSize, self.hmm.obsSize)
        
        for i in self.stateInd :
            newHmm.setPii( i,  gamma[1, i] )
            
            for j in self.stateInd :
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
            