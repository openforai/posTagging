#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 24, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

import sys
import numpy as np
import re

import dataProcessing.ioOperation as iop
import dataProcessing.templateFileName as templateFileName

unknownPOS = "UnknownPOS"


def formatTag(testRes, testedWords, resTested, trueWords, resTrue, words, pos):
    
    ex = r"^\d+((\.\d+)|(/\d+))?$"
    
    tested = testedWords.split('/')
    truth = trueWords.split('/')
    state = True
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
            state = False
            
    elif (len(tested) != len(truth)):
        print " \n\n AN ERROR ENCOUNTERED WITH WORDS MATCHING. SKIPPED : \n"
        print tested[0] + ", --> " + resTested
        print truth[0] + ", -->" + resTrue
        print testRes
        state = False        
    
    if( tested[0] != truth[0] ):
        print " \n\n AN ERROR ENCOUNTERED WITH WORDS MATCHING. SKIPPED : \n"
        print tested[0] + ", --> " + resTested
        print truth[0] + ", -->" + resTrue
        print testRes
        state = False
        
    return (tested, truth, state)


def buildNMostPos(pos, posFreq, n):
    
    mostPos = list()
    freq = np.zeros(n+1, dtype='int')
        
    for i in range(n):
        mostPos.append('0')
        
    #print mostPos
    #print freq
    
    for i in range(len(pos)):
          
        p = pos[i]
        f = posFreq[p]
        
        #print " Inserting {0} : {1}".format(p,f)
        
        if f > freq[n-1]:
            freq[n-1] = f
            mostPos[n-1] = p
            
            j = n-1
            
            while( (j > 0) and freq[j-1] < freq[j]):
                
                tmpP = mostPos[j]
                tmpF = freq[j]
                
                mostPos[j] = mostPos[j-1]
                freq[j] = freq[j-1]
                
                mostPos[j-1] = tmpP
                freq[j-1] = tmpF
                
                j -= 1
                
        #print mostPos
        #print freq
    
    mostPos.append(unknownPOS)
        
    return mostPos, freq
                    
                       
def confMatAllWords(testRes, testTrue, words, pos):
    
    conf = np.zeros((len(pos), len(pos)), dtype='int')
    
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
            
            (tested, truth, state) = formatTag(testRes, testedWords[c], resTested, trueWords[c], resTrue, words, pos)
            #print tested, truth
            if( state ) :
                
                if ( tested[1] in pos ) :    
                    j = pos.index(tested[1])
                else :
                    j = len(pos) - 1
                    #print " Words not handled : ", tested, truth
                
                if  ( truth[1] in pos ) :
                    i = pos.index(truth[1])
                else :                    
                    i = len(pos) - 1
                    #print " Words not handled : ", tested, truth
                    
                conf[i, j] += 1
            
    
    #print conf
    #print "Percentage Correct: ",np.trace(conf)/np.sum(conf)*100
    return conf
     

def confMatUnknownWords(testRes, testTrue, words, pos):
    
    #print "\n Computing Confusion matrice for unknown words..."
    
    conf = np.zeros((len(pos), len(pos)), dtype='int')
    ex = r"^\d+((\.\d+)|(/\d+))?$"
    count = 0
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
            
            (tested, truth, state) = formatTag(testRes, testedWords[c], resTested, trueWords[c], resTrue, words, pos)
            
            if( state ) :
            
                if (re.search(ex, tested[0]) is not None):            
                    tested[0] = '0'
            
                if (tested[0] not in words) :                    
                        
                    if ( tested[1] in pos ) :    
                        j = pos.index(tested[1])
                    else :
                        j = len(pos) - 1
                        #print " Words not handled : ", tested, truth
                    
                    if  ( truth[1] in pos ) :
                        i = pos.index(truth[1])
                    else :
                        i = len(pos) - 1
                            
                    
                    conf[i, j] += 1
                    count += 1
                   
    #print conf
    #print "Percentage Correct: ",np.trace(conf)/np.sum(conf)*100
    return conf


def confMatAmbiguousWords(testRes, testTrue, words, ambiguousWords, pos):
    
    #print "\n Computing Confusion matrice for Ambiguous words..."
    
    conf = np.zeros((len(pos), len(pos)), dtype='int')
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
            
            (tested, truth, state) = formatTag(testRes, testedWords[c], resTested, trueWords[c], resTrue, words, pos)
            
            if( state ) :
            
                if (re.search(ex, tested[0]) is not None):            
                    tested[0] = '0'
            
                if (tested[0] in ambiguousWords):
                    
                    if ( tested[1] in pos ) :    
                        j = pos.index(tested[1])
                    else :
                        j = len(pos) - 1
                        #print " Words not handled : ", tested, truth
                    
                    if  ( truth[1] in pos ) :                        
                        i = pos.index(truth[1])
                    else :
                        i = len(pos) - 1
                            
                    
                    conf[i, j] += 1
                    
                elif (tested[0] in ambiguousWords) :
                    #print " Ambiguous Words not handled : ", tested, truth
                    pass   
                            
    
    #print conf
    #print "Nb Training Ambiguous Words : ", nbDistAmbWords - int(np.sum(conf))
    #print "Nb Testing Ambiguous Words : ", int(np.sum(conf))
    #print "Percentage Correct: ",np.trace(conf)/np.sum(conf)*100.0
    
    return conf
        

def randResultAnalysis(tfn, model ):
        
        for model in models:
        
            print("\n\n\n\n\n*********************************************************")
            print("*                                                       *")
            print("*    {0} Rand Testing Result Analysis                   *".format(model))
            print("*                                                       *")
            print("*********************************************************\n\n")
            
           
            tfn.builfResultFile(model)
            posFreq = iop.readPosFreq(tfn.benchPosFreq)
            
            print " FILE : " + tfn.benchRandResultTagging + "\n"
            
            words = iop.readWords(tfn.benchRandWords)
            posOr = iop.readPos(tfn.benchRandCategories)
            
            #pos.append(unknownPOS) # tag used in ENN
            meta = iop.readMetaData(tfn.benchMeta)
            nbDistAmbWords = meta[5]
            
            maxPos = len(posOr) #meta[4]
            
            ambiguousWords = iop.readAmbiguousWords(tfn.benchAmbiguousWords)
            
            pos, freq = buildNMostPos(posOr, posFreq, maxPos)
            
            #print posOr
            print pos
            
            print "---> All Words : "
            conf = confMatAllWords(tfn.benchRandResultTagging, tfn.benchRandTestParsed, words, pos)
            print"\t\t - Percentage = ", float(np.trace(conf[:-1,:-1]))/np.sum(conf[:-1,:])*100
            
            print "\n---> Unknown Words : "
            conf = confMatUnknownWords(tfn.benchRandResultTagging, tfn.benchRandTestParsed, words, pos)
            print"\n\t\t - Percentage = ", float(np.trace(conf[:-1,:-1]))/np.sum(conf[:-1,:])*100
            
            print "\n---> Ambiguous Words : "
            conf = confMatAmbiguousWords(tfn.benchRandResultTagging, tfn.benchRandTestParsed, words, ambiguousWords, pos)
            
            print"\t\t - Percentage = ", float(np.trace(conf[:-1,:-1]))/np.sum(conf[:-1,:])*100
            print"\t\t - Nb Ambiguous Words = ",nbDistAmbWords
            print"\t\t - Nb Ambiguous Words in Training Set  = ",nbDistAmbWords - np.sum(conf)
            print"\t\t - Nb Ambiguous Words in Testing Set = ", np.sum(conf[:-1,:])
            
            #mostPos, freq = buildNMostPos(pos[:-1], posFreq, mostAppear)
            mostPos = pos[:mostAppear]
            mostPos.append(unknownPOS)
            print "\n\n---> Most Appeared POS : ", mostPos
                    
            print "\n\n---> All Words For Most POS : "
            conf = confMatAllWords(tfn.benchRandResultTagging, tfn.benchRandTestParsed, words, mostPos)
            print"\t\t - Percentage = ", float(np.trace(conf[:-1,:-1]))/np.sum(conf[:-1,:])*100
            print"\t\t - Conf Mat : "
            print conf
            
            print "---> Unknown Words For Most POS : "
            conf = confMatUnknownWords(tfn.benchRandResultTagging, tfn.benchRandTestParsed, words, mostPos)
            print"\t\t - Percentage = ", float(np.trace(conf[:-1,:-1]))/np.sum(conf[:-1,:])*100
            print"\t\t - Conf Mat : "
            print conf
            
            print "---> Ambiguous Words For Most POS : "
            conf = confMatAmbiguousWords(tfn.benchRandResultTagging, tfn.benchRandTestParsed, words, ambiguousWords, mostPos)
            
            print"\t\t - Percentage = ", float(np.trace(conf[:-1,:-1]))/np.sum(conf[:-1,:])*100
            #print"\t\t - Nb Training Ambiguous Words = ",nbDistAmbWords - np.sum(conf)
            #print"\t\t - Nb Testing Ambiguous Words = ", np.sum(conf)
            print"\t\t - Conf Mat : "
            print conf


def allCrossResultAnalysis(tfn, model ):
        
        for model in models:
            
                            
            confAllWordsAllPost = 0
            confUnknWordsAllPost = 0
            confAmbWordsAllPost = 0
            
            confAllWordsMostPost = 0
            confUnknWordsMostPost = 0
            confAmbWordsMostPost = 0
        
            print("\n\n\n\n\n*********************************************************")
            print("*                                                       *")
            print("*    {0} Cross Testing Result Analysis                   *".format(model))
            print("*                                                       *")
            print("*********************************************************\n\n")
            
            for cnum in range(1, maxCross+1):
            
                print("\n\n************{0} Cross Testing Result Analysis {1}************\n".format(model, cnum))
                
                tfn.buildForCross(cnum)
                tfn.builfResultFile(model, cnum)
                
                print " FILE : " + tfn.benchCrossResultTagging + "\n"
                
                confMatUnknownWords
                posFreq = iop.readPosFreq(tfn.benchPosFreq)
            
                words = iop.readWords(tfn.benchCrossWords)
                posOr = iop.readPos(tfn.benchCrossCategories)
                
                #pos.append(unknownPOS) # tag used in ENN
                meta = iop.readMetaData(tfn.benchMeta)                
                nbDistAmbWords = meta[5]
                
                maxPos = meta[4]#len(posOr)
                
                ambiguousWords = iop.readAmbiguousWords(tfn.benchAmbiguousWords)
                
                pos, freq = buildNMostPos(posOr, posFreq, maxPos)
                
                #print posOr
                print pos
                
                confAllWordsAllPost += confMatAllWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, pos)
                
                
                confUnknWordsAllPost += confMatUnknownWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, pos)
                
                confAmbWordsAllPost += confMatAmbiguousWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, ambiguousWords, pos)
               
               
                #mostPos, freq = buildNMostPos(posOr[:-1], posFreq, mostAppear)
                mostPos = pos[:mostAppear]
                mostPos.append(unknownPOS)
                
                confAllWordsMostPost += confMatAllWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, mostPos)
                
                
                confUnknWordsMostPost += confMatUnknownWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, mostPos)
                
                confAmbWordsMostPost += confMatAmbiguousWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, ambiguousWords, mostPos)
                
            confAllWordsAllPost = confAllWordsAllPost# / maxCross
            confUnknWordsAllPost = confUnknWordsAllPost# / maxCross
            confAmbWordsAllPost = confAmbWordsAllPost# / maxCross
            
            confAllWordsMostPost = confAllWordsMostPost# / maxCross
            confUnknWordsMostPost = confUnknWordsMostPost# / maxCross
            confAmbWordsMostPost = confAmbWordsMostPost# / maxCross
            
            print "\n\n : Result : "     
            print "---> All Words : "
            print"\t\t - Percentage = ", float(np.trace(confAllWordsAllPost[:-1,:-1]))/np.sum(confAllWordsAllPost[:-1,:])*100
            
            print "\n---> Unknown Words : "
            print"\n\t\t - Percentage = ", float(np.trace(confUnknWordsAllPost[:-1,:-1]))/np.sum(confUnknWordsAllPost[:-1,:])*100
            
            print "\n---> Ambiguous Words : "                 
            print"\t\t - Percentage = ", float(np.trace(confAmbWordsAllPost[:-1,:-1]))/np.sum(confAmbWordsAllPost[:-1,:])*100
            print"\t\t - Nb Ambiguous Words = ",nbDistAmbWords * maxCross
            print"\t\t - Nb Ambiguous Words in Training Set  = ",(nbDistAmbWords * maxCross) - np.sum(confAmbWordsAllPost)
            print"\t\t - Nb Ambiguous Words in Testing Set = ", np.sum(confAmbWordsAllPost[:-1,:])
            
            print "\n\n---> Most Appeared POS : ", mostPos
                    
            print "\n\n---> All Words For Most POS : "
            print"\t\t - Percentage = ", float(np.trace(confAllWordsMostPost[:-1,:-1]))/np.sum(confAllWordsMostPost[:-1,:])*100
            print"\t\t - Conf Mat : "
            print confAllWordsMostPost
            
            print "---> Unknown Words For Most POS : "
            print"\t\t - Percentage = ", float(np.trace(confUnknWordsMostPost[:-1,:-1]))/np.sum(confUnknWordsMostPost[:-1,:])*100
            print"\t\t - Conf Mat : "
            print confUnknWordsMostPost
            
            print "---> Ambiguous Words For Most POS : "                
            print"\t\t - Percentage = ", float(np.trace(confAmbWordsMostPost[:-1,:-1]))/np.sum(confAmbWordsMostPost[:-1,:])*100
            #print"\t\t - Nb Training Ambiguous Words = ",nbDistAmbWords - np.sum(conf)
            #print"\t\t - Nb Testing Ambiguous Words = ", np.sum(conf)
            print"\t\t - Conf Mat : "
            print confAmbWordsMostPost


def oneCrossResultAnalysis(tfn, model, cnum ):
        
        for model in models:
                   
            print("\n\n\n\n\n*********************************************************")
            print("*                                                       *")
            print("*    {0} Cross Testing Result Analysis                   *".format(model))
            print("*                                                       *")
            print("*********************************************************\n\n")
            
            
            
            print("\n\n************{0} Cross Testing Result Analysis {1}************\n".format(model, cnum))
            
            tfn.buildForCross(cnum)
            tfn.builfResultFile(model, cnum)
            
            print " FILE : " + tfn.benchCrossResultTagging + "\n"
            
            #confMatUnknownWords
            posFreq = iop.readPosFreq(tfn.benchPosFreq)
        
            words = iop.readWords(tfn.benchCrossWords)
            posOr = iop.readPos(tfn.benchCrossCategories)
            
            #pos.append(unknownPOS) # tag used in ENN
            meta = iop.readMetaData(tfn.benchMeta)            
            nbDistAmbWords = meta[5]
            
            maxPos = len(posOr) #meta[4]
            
            ambiguousWords = iop.readAmbiguousWords(tfn.benchAmbiguousWords)
            
            pos, freq = buildNMostPos(posOr, posFreq, maxPos)
            
            #print posOr
            print pos
            
            confAllWordsAllPost = confMatAllWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, pos)
            
            
            confUnknWordsAllPost = confMatUnknownWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, pos)
            
            confAmbWordsAllPost = confMatAmbiguousWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, ambiguousWords, pos)
           
           
            #mostPos, freq = buildNMostPos(posOr, posFreq, mostAppear)
            mostPos = pos[:mostAppear]
            mostPos.append(unknownPOS)
            
            confAllWordsMostPost = confMatAllWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, mostPos)
            
            
            confUnknWordsMostPost = confMatUnknownWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, mostPos)
            
            confAmbWordsMostPost = confMatAmbiguousWords(tfn.benchCrossResultTagging, tfn.benchCrossTestParsed, words, ambiguousWords, mostPos)
            
            print "\n\n : Result : "     
            print "---> All Words : "
            print"\t\t - Percentage = ", float(np.trace(confAllWordsAllPost[:-1,:-1]))/np.sum(confAllWordsAllPost[:-1,:])*100
            
            print "\n---> Unknown Words : "
            print"\n\t\t - Percentage = ", float(np.trace(confUnknWordsAllPost[:-1,:-1]))/np.sum(confUnknWordsAllPost[:-1,:])*100
            
            print "\n---> Ambiguous Words : "                 
            print"\t\t - Percentage = ", float(np.trace(confAmbWordsAllPost[:-1,:-1]))/np.sum(confAmbWordsAllPost[:-1,:])*100
            print"\t\t - Nb Ambiguous Words = ",nbDistAmbWords
            print"\t\t - Nb Ambiguous Words in Training Set  = ",nbDistAmbWords - np.sum(confAmbWordsAllPost)
            print"\t\t - Nb Ambiguous Words in Testing Set = ", np.sum(confAmbWordsAllPost[:-1,:])
            
            print "\n\n---> Most Appeared POS : ", mostPos
                    
            print "\n\n---> All Words For Most POS : "
            print"\t\t - Percentage = ", float(np.trace(confAllWordsMostPost[:-1,:-1]))/np.sum(confAllWordsMostPost[:-1,:])*100
            print"\t\t - Conf Mat : "
            print confAllWordsMostPost
            
            print "---> Unknown Words For Most POS : "
            print"\t\t - Percentage = ", float(np.trace(confUnknWordsMostPost[:-1,:-1]))/np.sum(confUnknWordsMostPost[:-1,:])*100
            print"\t\t - Conf Mat : "
            print confUnknWordsMostPost
            
            print "---> Ambiguous Words For Most POS : "                
            print"\t\t - Percentage = ", float(np.trace(confAmbWordsMostPost[:-1,:-1]))/np.sum(confAmbWordsMostPost[:-1,:])*100
            #print"\t\t - Nb Training Ambiguous Words = ",nbDistAmbWords - np.sum(conf)
            #print"\t\t - Nb Testing Ambiguous Words = ", np.sum(conf)
            print"\t\t - Conf Mat : "
            print confAmbWordsMostPost

                

if __name__ == '__main__':    
    
    #print(sys.argv)
    
    base = sys.argv[1]
    bench = sys.argv[2]
    maxCross = int(sys.argv[3])
    cnum = int(sys.argv[3])
    mostAppear = int(sys.argv[4])
    models = []
    models.append('BLM')
    models.append('HMM')
    #models.append('ENN')
    
    print("\nRESULT ANALYSIS ... For Models {0}\n".format(models))

    tfn = templateFileName.TemplateFileName(base, bench)
    
    #randResultAnalysis(tfn, models)
    
    allCrossResultAnalysis(tfn, models)
    
    #oneCrossResultAnalysis(tfn, models, cnum)            

        #print "Cross Analysing"
        #crossResAnalyser(tfn, model)
        
    
    
    print "\n\n\n\n RESULT ANALYSIS ENDED."