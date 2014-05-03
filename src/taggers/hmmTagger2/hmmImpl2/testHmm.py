#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Nov 2, 2013

@author: Paulin AMOUGOU
'''

from hmm import HMM
from forwardBackward import ForwardBackward
from baumWelch import BaumWelch

import viterbi

import numpy as np
from StringIO import StringIO
 
pi = 0.3333333333 # Equi probabilty
aij = 0.3333333333 # Equi probability
nbState = 3
nbObs = 2
obs = ["H", "T"]

opdf = " 0.5 0.5\n 0.75 0.25\n 0.25 0.75"
bik = np.genfromtxt(StringIO(opdf), delimiter=' ')
oseq = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 1])


hmm = HMM(nbState, nbObs)

for i in range( nbState ):
    
    hmm.setPii(i, pi)
    
    for k in range( nbObs ):
        hmm.setBik( i, k, bik[i,k] )

for i in range( nbState ):
    for j in range( nbState ):
        hmm.setAij(i, j, aij)
     
hmm.display()


bestPath = viterbi.viterbiProcessing(hmm, oseq)
print("Best Path : {0}, p = {1}".format(bestPath[0], bestPath[1]))
  
fwbw = ForwardBackward(hmm, oseq, False, True)
print("Probabilty of {0} is {1}".format(oseq, fwbw.probability) )
  
print("Baum Welch processing ...")
  
oldHmm = hmm
oldP = bestPath[1]
for i in range(1,11):
    print("\n\n Iteration {0} : \n".format(i))
    baum = BaumWelch()
    newHmm = baum.learn(oldHmm, oseq)
      
    newHmm.display()
      
    bestPath = viterbi.viterbiProcessing(newHmm, oseq)
    print("Best Path : {0}, p = {1}".format(bestPath[0], bestPath[1]))
      
    fwbw = ForwardBackward(newHmm, oseq, False, True)
    print("Probabilty of {0} is {1}".format(oseq, fwbw.probability) )
      
    if( bestPath[1] > oldP ) :
        oldHmm = newHmm
        oldP = bestPath[1]
    else:
        print("Best Model founded at iteration {0}.".format(i))
        break
