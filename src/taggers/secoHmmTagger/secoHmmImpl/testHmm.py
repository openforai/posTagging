#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Nov 2, 2013

@author: Paulin AMOUGOU
'''

from secoHmm import SecoHMM
#from forwardBackward import ForwardBackward
#from baumWelch import BaumWelch

import viterbi

import numpy as np
from StringIO import StringIO
 
pi = 0.3333333333 # Equi probabilty
aijk = 0.3333333333 # Equi probability
nbState = 3
nbObs = 2
obs = ["H", "T"]

opdf = " 0.5 0.5\n 0.75 0.25\n 0.25 0.75"
bijk = np.genfromtxt(StringIO(opdf), delimiter=' ')
oseq = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 1])


secoHmm = SecoHMM(nbState, nbObs)

for i in range( nbState ):
    
    secoHmm.setPii(i, pi)
    
    for j in range( nbState ):
        for k in range( nbObs ):
            secoHmm.setBijk( i, j, k, bijk[i,k] )

for i in range( nbState ):
    for j in range( nbState ):
        for k in range( nbState ):
            secoHmm.setAijk(i, j, k, aijk)
     
secoHmm.display()

bestPath = viterbi.viterbiProcessing(secoHmm, oseq)
print("Best Path : {0}, p = {1}".format(bestPath[0], bestPath[1]))
exit()  
fwbw = ForwardBackward(secoHmm, oseq, False, True)
print("Probabilty of {0} is {1}".format(oseq, fwbw.probability) )
  
print("Baum Welch processing ...")
  
oldHmm = secoHmm
oldP = bestPath[1]
for i in range(1,11):
    print("\n\n Iteration {0} : \n".format(i))
    baum = BaumWelch()
    newHmm = baum.learn(oldHmm, oseq)
      
    newHmm.display()
      
    bestPath = viterbi.viterbiProcessing(newHmm, oseq)
    print("Best Path : {0}, p = {1}".format(bestPath[0], bestPath[1]))
      
    fwbw = ForwardBackward(newHmm, oseq, False, True)
    print("Probability of {0} is {1}".format(oseq, fwbw.probability) )
      
    if( bestPath[1] > oldP ) :
        oldHmm = newHmm
        oldP = bestPath[1]
    else:
        print("Best Model founded at iteration {0}.".format(i))
        break
