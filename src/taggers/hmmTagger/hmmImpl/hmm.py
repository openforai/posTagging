#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Oct 5, 2013

@author: Paulin AMOUGOU
'''
import numpy as np

class HMM(object):
    
    def __init__(self, stateSize, obsSize):
        
        self.states = list()
        self.observables = list()
        
        self.a = np.zeros( (stateSize, stateSize) )
        self.b = np.zeros( (stateSize, obsSize) )
        self.pi = np.zeros( stateSize )
        
        self._stateSize = stateSize
        self._obsSize = obsSize
        
        #print(self.a)
        #print(self.b)
        #print(self.pi)        
    
    def _getStateSize(self):       
        return self._stateSize
    
    def _setStateSize(self, dummy):
        '''
        Once build, the HMM state size never changes 
        '''
        print ("Once build, the HMM state size never changes")
        
        
    def _getObsSize(self):        
        return self._obsSize
    
    def _setObsSize(self, dummy):
        '''
        Once build, the HMM observable state never changes
        '''
        print ("Once build, the HMM observable state never changes")
            
                 
    def getAij(self, i, j):
        return self.a[i,j]
    
    def setAij(self, i, j, aij):
        self.a[i,j] = aij
    
    def getBik(self, i, k, ):
        return self.b[i,k]
        
    def setBik(self, i, k, bik):
        self.b[i,k] = bik
        
    def getPii(self, i):
        return self.pi[i]
        
    def setPii(self, i, pi):
        self.pi[i] = pi
    
    
    def display(self):
        
        print("Nb State : ", self.stateSize)
        print("NB Observbles : ", self.obsSize)
        print("Initial probabilities")
        print(self.pi)
        print(" State Transition")
        print(self.a)
        print("Distribution Probabilities")
        print(self.b)
    
    obsSize = property(_getObsSize, _setObsSize)
    stateSize = property(_getStateSize, _setStateSize)