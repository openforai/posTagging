#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Nov 18, 2013

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''


# Code from Chapter 3 of Machine Learning: An Algorithmic Perspective
# by Stephen Marsland (http://seat.massey.ac.nz/personal/s.r.marsland/MLBook.html)

# You are free to use, change, or redistribute the code in any way you wish for
# non-commercial purposes, but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Stephen Marsland, 2008

import numpy as np

expValMax = 45

class EMLP:
    """ A Multi-Layer Perceptron With Elastic Input"""
    
    def __init__(self, nout, l=3, r=3, beta=1, momentum=0.9):
        """ Constructor """
        
        # Set up network size
        self.nin = nout * (l + r + 1) # (l,r)
        self.nout = nout
        self.nhidden = self.nin / 2
        self.nacthidden =  nout # the update will be called before, to increase it to l=1 and r=1
                
        print "nin {0} nout {1} nhidden {2}".format( self.nin, self.nout, self.nhidden)
        
        self.l = l
        self.r = r

        self.beta = beta
        self.momentum = momentum
        
        np.random.seed()
        
        # Initialized network weight
        self.hidw = (np.random.rand(self.nin+1,self.nhidden)-0.5)*2/np.sqrt(self.nin)
        self.outw = (np.random.rand(self.nhidden+1,self.nout)-0.5)*2/np.sqrt(self.nhidden)
        
        # Initialized network weight updater
        self.uphidw = np.zeros((self.nin+1,self.nhidden))
        self.upoutw = np.zeros((self.nhidden+1,self.nout))
        
        # Initialized network weight temp updater
        self.tempuphidw = np.zeros((self.nin+1,self.nhidden))
        self.tempupoutw = np.zeros((self.nhidden+1,self.nout))
        
        self.error = 0.0
        
        #print self.hidw
        #print self.outw
                    
    
    def updateLR(self, newl, newr):
        
        self.l = newl
        self.r = newr
        
        self.nacthidden = ((newl + newr + 1) * self.nout) / 2
        
        self.uphidw.fill(0.0)
        self.upoutw.fill(0.0)
        self.error = 0.0
        
        #print " New hidden : ", self.nacthidden
    
    
    def computeActivation(self, outputs):
        
        global expValMax
        
        for i in range(np.shape(outputs)[0]):
            for j in range(np.shape(outputs)[1]):
                
                if outputs[i,j] < (-1*expValMax) :
                    outputs[i,j] = 0.0
                elif outputs[i,j] > expValMax :
                    outputs[i,j] = 1.0
                else:
                    outputs[i,j] = 1.0/(1.0+np.exp(outputs[i,j]))
            
        #print outputs
        return outputs
        
        
    def forward(self, inputs):
        """ Run the network forward """
        #print(np.shape(inputs))
        #print(np.shape(self.weights1))
        self.ahid = np.dot(inputs, self.hidw)
        
        self.ahid = 0.5 * (1+np.tanh(self.ahid))#self.computeActivation( -self.beta * self.ahid )
        
        self.ahid[:, self.nacthidden:] = 0.0  # cancel activation for non use hidden neural
        
        self.ahid = np.concatenate((self.ahid,-np.ones((np.shape(inputs)[0],1))),axis=1) # Add the inputs that match the bias node

        self.outputs = np.dot(self.ahid, self.outw)
       
        self.outputs = 0.5 * (1+np.tanh(self.outputs))#self.computeActivation( -self.beta * self.outputs )        
        
        return self.outputs
        

    def backwardInter(self, inputs, targets, eta):
        
        """ First part of back propagate """ 
        
        self.error += 0.5*np.sum((targets-self.outputs)**2)                
        
        #deltao = (targets-self.outputs)*self.outputs*(1.0-self.outputs)
        deltao = (targets-self.outputs)*(1.0-self.outputs**2)
        
        #deltah = self.ahid*(1.0-self.ahid)*(np.dot(deltao,np.transpose(self.outw)))
        deltah = (1.0-self.ahid**2)*(np.dot(deltao,np.transpose(self.outw)))

        self.tempuphidw += eta*(np.dot(np.transpose(inputs), deltah[:,:-1]))
        self.tempupoutw += eta*(np.dot(np.transpose(self.ahid), deltao))
        
                 
    def backward(self, inputs, targets, eta):
        
        """ First part of back propagate """ 
        
        self.error = 0.5*np.sum((targets-self.outputs)**2)
        
        #print " Error In Training: ", self.error                
        
        #deltao = (targets-self.outputs)*self.outputs*(1.0-self.outputs)
        deltao = (targets-self.outputs)*(1.0-self.outputs**2)
        
        #deltah = self.ahid*(1.0-self.ahid)*(np.dot(deltao,np.transpose(self.outw)))
        deltah = (1.0-self.ahid**2)*(np.dot(deltao,np.transpose(self.outw)))

        #self.uphidw = np.zeros((self.nin+1,self.nhidden))
        #self.upoutw = np.zeros((self.nhidden+1,self.nout))
        
        self.uphidw = eta*(np.dot(np.transpose(inputs), deltah[:,:-1])) + self.momentum*self.uphidw
        self.upoutw = eta*(np.dot(np.transpose(self.ahid), deltao)) + self.momentum*self.upoutw
        
        self.hidw += self.uphidw
        self.outw += self.upoutw
        
                   
    def weightUpdate(self):
        
        self.uphidw = self.tempuphidw + self.momentum*self.uphidw
        self.upoutw = self.tempupoutw + self.momentum*self.upoutw
        
        self.hidw += self.uphidw
        self.outw += self.upoutw
        
        self.tempuphidw.fill(0.0)
        self.tempupoutw.fill(0.0)
        
        #print self.hidw
        #print self.outw
        
        
    def fwdBackwdBatch(self, inputs, targets, eta):
        
        out = self.forward(inputs)
        
        #print out
        
        self.backwardInter(inputs, targets, eta)
        
        
    def fwdBackwd(self, inputs, targets, eta):
        
        out = self.forward(inputs)
        
        #print out
        
        self.backward(inputs, targets, eta)
        
    
    def saveWeight(self):
        
        self.hidwSaved = self.hidw
        self.outwSaved = self.outw
        
        
    def restoreOldWeight(self):
        
        self.hidwd = self.hidwSave
        self.outw = self.outwSaved
        
        
    def confmat(self,inputs,targets):
        """Confusion matrix"""

        # Add the inputs that match the bias node
        inputs = np.concatenate((inputs,-np.ones((np.shape(inputs)[0],1))),axis=1)
        outputs = self.forward(inputs)
        #print("BEFOR Comfmat Outputs : {0}".format(outputs))
        #print("BEFOR Comfmat Targets : {0}".format(targets))
        nclasses = np.shape(targets)[1]

        if nclasses==1:
            nclasses = 2
            outputs = np.where(outputs>0.5,1,0)
        else:
            # 1-of-N encoding
            outputs = np.argmax(outputs,1)
            targets = np.argmax(targets,1)

        #print("AFTER Comfmat Outputs : {0}".format(outputs))
        #print("AFTER Comfmat Targets : {0}".format(targets))
        cm = np.zeros((nclasses,nclasses))
        for i in range(nclasses):
            for j in range(nclasses):
                #print where(outputs==i,1,0)
                cm[i,j] = np.sum(np.where(outputs==i,1,0)*np.where(targets==j,1,0))

        print "Confusion matrix is:"
        print cm
        print "Percentage Correct: ",np.trace(cm)/np.sum(cm)*100


def demo():
    
    anddata = np.array([[0,0,0],[0,1,0],[1,0,0],[1,1,1]])
    
    emlp = EMLP(1, 0, 1)
    
    train = np.concatenate((anddata[:,0:2], -np.ones((np.shape(anddata)[0],1))),axis=1 )
    target = anddata[:,2:3]
    
    for i in range(3):
        
        print "Iteration : ", i
        
        emlp.fwdBackwd2(train[0:2,:], target[0:2,:], 0.1)
        emlp.fwdBackwd2(train[2:2,:], target[2:2,:], 0.1)
        emlp.weightUpdate()
        
        #emlp.fwdBackwd(train, target, 0.1)
        
    emlp.confmat(anddata[:,0:2],anddata[:,2:3])
    
    

if __name__ == '__main__':    
    
    demo()
    