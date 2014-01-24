#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Jan 21, 2014

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

class TemplateFileName(object):
    
    def __init__(self, base, bench):

        if(bench.lower() == 'brown'):
            self.baseBench = base + '/brown/'
            self.benchFiles = self.baseBench + 'brownBench.txt'
            
            self.mainBenchBase = self.baseBench + 'mainData/'            
            self.benchWordsDico = self.mainBenchBase + 'brownWordsDico.pickle'
            self.benchPosDico = self.mainBenchBase + 'brownPosDico.pickle'
            self.benchMeta =  self.mainBenchBase + 'brownMetaData.txt'
            self.benchCategories = self.mainBenchBase + 'brownCategories.pickle'
            self.benchWords = self.mainBenchBase + 'brownWords.pickle'
            self.benchTrain =  self.mainBenchBase + 'brownAllPhrases.txt'
            self.benchError =  self.mainBenchBase + 'brownErrors.txt'
            
            self.baseRandBench = self.baseBench + 'randomTest/'
            self.benchRandWordsDico = self.baseRandBench + 'brownWordsDico.pickle'
            self.benchRandPosDico = self.baseRandBench + 'brownPosDico.pickle'
            self.benchRandMeta =  self.baseRandBench + 'metaData.txt'
            self.benchRandCategories = self.baseRandBench + 'categories.pickle'
            self.benchRandWords = self.baseRandBench + 'words.pickle'
            self.benchRandTrain =  self.baseRandBench + 'trainingPhrases.txt'
            self.benchRandTrainInd =  self.baseRandBench + 'trainingPhrases_ind.txt'
            self.benchRandTest =  self.baseRandBench + 'testPhrases.txt'
            self.benchRandTestParsed =  self.baseRandBench + 'testParsedPhrases.txt'            
            self.benchRandError =  self.baseRandBench + 'brownErrors.txt'
            
            self.baseCrossBenchMain = self.baseBench + 'crossingTest/'
            self.tmpBenchCross = self.baseCrossBenchMain + 'tmpBenchCross'
            self.benchCrossFiles = self.baseCrossBenchMain + 'data/cross_{0}'
            
        elif(bench.lower() == 'penn'):
            print("\n\n SORRY, \n\t PENN BENCHMARK IS NOT YET TREATED")
            exit()
            
        else:
            print("UNKNOW BENCHMARK NAME '{0}'. Please provide 'brown' or 'penn' : ".format(bench))
            exit()
            
            
    def buildForCross(self, crossNum):
        
        self.baseCrossBenchSub = self.baseCrossBenchMain + 'test_{0}/'
        self.baseCrossBenchSub = self.baseCrossBenchSub.format(crossNum)
        
        self.benchCrossWordsDico = self.baseCrossBenchSub + 'brownWordsDico.pickle'
        self.benchCrossPosDico = self.baseCrossBenchSub + 'brownPosDico.pickle'
        self.benchCrossMeta =  self.baseCrossBenchSub + 'metaData.txt'
        self.benchCrossCategories = self.baseCrossBenchSub + 'categories.pickle'
        self.benchCrossWords = self.baseCrossBenchSub + 'words.pickle'
        self.benchCrossTrain =  self.baseCrossBenchSub + 'trainingPhrases.txt'
        self.benchCrossTrainInd =  self.baseCrossBenchSub + 'trainingPhrases_ind.txt'
        self.benchCrossTest =  self.baseCrossBenchSub + 'testPhrases.txt'
        self.benchCrossTestParsed =  self.baseCrossBenchSub + 'testParsedPhrases.txt'
        self.benchCrossError =  self.baseCrossBenchSub + 'brownErrors.txt'
        
    
    def builfResultFile(self, model, crossNum=0):
        
        if( model.lower() == 'blm'):
            self.benchTestBase = self.baseBench + 'testResult/blm/'
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            
        elif ( model.lower() == 'hmm'):
            self.benchTestBase = self.baseBench + 'testResult/hmm/'
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
        
        elif ( model.lower() == 'enn'):
            self.benchTestBase = self.baseBench + 'testResult/enn/'
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
        
        #print self.benchRandResultTagging
        #print self.benchCrossResultTagging        