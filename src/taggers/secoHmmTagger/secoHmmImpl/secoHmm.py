#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Oct 5, 2013

@author: Paulin AMOUGOU
'''
import numpy as np

class SecoHMM(object):
    
    def __init__(self, stateSize, obsSize):
        
        self.states = list()
        self.observables = list()
        
        self.a = np.zeros( (stateSize, stateSize, stateSize) )
        self.b = np.zeros( (stateSize, stateSize, obsSize) )
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
            
                 
    def getAijk(self, i, j, k):
        return self.a[i,j,k]
    
    def setAijk(self, i, j, k, aijk):
        self.a[i,j,k] = aijk
    
    def getBijk(self, i, j, k ):
        return self.b[i,j,k]
        
    def setBijk(self, i, j, k, bijk):
        self.b[i,j,k] = bijk
        
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