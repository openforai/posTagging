#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 24, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

import sys
import time
import numpy as np
import re

import dataProcessing.ioOperation as iop
import dataProcessing.templateFileName as templateFileName


def confMatAllWords(testRes, testTrue, words, pos):
    
    conf = np.zeros((len(pos), len(pos)))
    ex = r"^\d+((\.\d+)|(/\d+))?$"
    
    for resTrue, resTested in iop.getNextTestedLine(testRes, testTrue):
        
        #print resTested
        #print resTrue
        #print "\n\n"
        
        trueWords = resTrue.strip().split(" ");
        testedWords = resTested.strip().split(" ");
        
        if( len(trueWords) != len(testedWords)):
            print " \n\n AN ERROR ENCOUNTERED WITH PHRASES LENGTH. SKIPPED : \n"
            print resTested
            print resTrue
            print testRes
            continue
        
        for c in range( len(trueWords) ):
            tested = testedWords[c].split('/')
            truth = trueWords[c].split('/')
            #print truth
            #print tested
            
            if ( (len(tested) == len(truth)) and (len(truth) == 3) ):
                    
                if ((re.search(ex, tested[0]+"/"+tested[1]) is not None) and (re.search(ex, truth[0]+"/"+truth[1]) is not None)):
                    tested[0] = tested[0]+"/"+tested[1] #Fraction
                    tested[1] = tested[2]
                    tested[2] = ""
                    
                    truth[0] = truth[0]+"/"+truth[1] #Fraction
                    truth[1] = truth[2]
                    truth[2] = ""
                    
                    #print truth
                    #print tested
                else:
                    print " \n\n AN ERROR ENCOUNTERED WITH WORDS MATCHING. SKIPPED : \n"
                    print tested[0] + ", --> " + resTested
                    print truth[0] + ", -->" + resTrue
                    print testRes
                    break
                    
            elif (len(tested) != len(truth)):
                print " \n\n AN ERROR ENCOUNTERED WITH WORDS MATCHING. SKIPPED : \n"
                print tested[0] + ", --> " + resTested
                print truth[0] + ", -->" + resTrue
                print testRes
                break
                
            
            if( tested[0] != truth[0] ):
                print " \n\n AN ERROR ENCOUNTERED WITH WORDS MATCHING. SKIPPED : \n"
                print tested[0] + ", --> " + resTested
                print truth[0] + ", -->" + resTrue
                print testRes
                break
                
            i = pos.index(truth[1])
            j = pos.index(tested[1])
            
            conf[i, j] += 1
            
    
    #print conf
    print "Percentage Correct: ",np.trace(conf)/np.sum(conf)*100
     

def confMatUnknownWords(testRes, testTrue, words, pos):
    
    print "\n Computing Confusion matrice ..."
    
    conf = np.zeros((len(pos), len(pos)))
    ex = r"^\d+((\.\d+)|(/\d+))?$"
    
    for resTrue, resTested in iop.getNextTestedLine(testRes, testTrue):
        
        #print resTested
        #print resTrue
        #print "\n\n"
        
        trueWords = resTrue.strip().split(" ");
        testedWords = resTested.strip().split(" ");
        
        if( len(trueWords) != len(testedWords)):
            print " \n\n AN ERROR ENCOUNTERED WITH PHRASES LENGTH. SKIPPED : \n"
            print resTested
            print resTrue
            print testRes
            continue
        
        for c in range( len(trueWords) ):
            tested = testedWords[c].split('/')
            truth = trueWords[c].split('/')
            #print truth
            #print tested
            
            if ( (len(tested) == len(truth)) and (len(truth) == 3) ):
                    
                if ((re.search(ex, tested[0]+"/"+tested[1]) is not None) and (re.search(ex, truth[0]+"/"+truth[1]) is not None)):
                    tested[0] = tested[0]+"/"+tested[1] #Fraction
                    tested[1] = tested[2]
                    tested[2] = ""
                    
                    truth[0] = truth[0]+"/"+truth[1] #Fraction
                    truth[1] = truth[2]
                    truth[2] = ""
                    
                    #print truth
                    #print tested
                else:
                    print " \n\n AN ERROR ENCOUNTERED WITH WORDS MATCHING. SKIPPED : \n"
                    print tested[0] + ", --> " + resTested
                    print truth[0] + ", -->" + resTrue
                    print testRes
                    break
                    
            elif (len(tested) != len(truth)):
                print " \n\n AN ERROR ENCOUNTERED WITH WORDS MATCHING. SKIPPED : \n"
                print tested[0] + ", --> " + resTested
                print truth[0] + ", -->" + resTrue
                print testRes
                break
                
            
            if( tested[0] != truth[0] ):
                print " \n\n AN ERROR ENCOUNTERED WITH WORDS MATCHING. SKIPPED : \n"
                print tested[0] + ", --> " + resTested
                print truth[0] + ", -->" + resTrue
                print testRes
                break
            
            if (re.search(ex, tested[0]) is not None):            
                tested[0] = '0'
        
            if tested[0] not in words:
                
                i = pos.index(truth[1])
                j = pos.index(tested[1])
                
                conf[i, j] += 1
            
    
    #print conf
    print "Percentage Correct: ",np.trace(conf)/np.sum(conf)*100

if __name__ == '__main__':    
    
    #print(sys.argv)
    
    base = sys.argv[1]
    bench = sys.argv[2]
    maxCross = int(sys.argv[3])
    models = ['BLM', 'HMM']
    
    print("\nRESULT ANALYSIS ...\n")

    tfn = templateFileName.TemplateFileName(base, bench)
    
    for model in models:
        
        print("\n\n************{0} Rand Testing Result Analysis************\n".format(model))
        
        tfn.builfResultFile(model)
        
        print " FILE : " + tfn.benchRandResultTagging + "\n"
        
        words = iop.readWords(tfn.benchRandWords)
        pos = iop.readPos(tfn.benchRandCategories)
        
        print "All Words \n"
        confMatAllWords(tfn.benchRandResultTagging, tfn.benchRandTestParsed, words, pos)
        
        print "Unknown Words \n"
        confMatUnknownWords(tfn.benchRandResultTagging, tfn.benchRandTestParsed, words, pos)
        
        for cnum in range(1, maxCross+1):
            
            print("\n\n************{0} Cross Testing Result Analysis {1}************\n".format(model, cnum))
            
            tfn.buildForCross(cnum)
            tfn.builfResultFile(model, cnum)
            
            print " FILE : " + tfn.benchCrossResultTagging + "\n"
            
            words = iop.readWords(tfn.benchCrossWords)
            pos = iop.readPos(tfn.benchCrossCategories)
        
            print "All Words \n"
            confMatAllWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, pos)
            
            print "Unknown Words \n"
            confMatUnknownWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, pos)
    
    
    print "\n\n RESULT ANALYSIS ENDED."