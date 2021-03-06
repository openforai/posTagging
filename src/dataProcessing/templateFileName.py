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
            self.benchPosFreq = self.mainBenchBase + 'brownPosFreq.pickle'
            self.benchMeta =  self.mainBenchBase + 'brownMetaData.txt'
            self.benchCategories = self.mainBenchBase + 'brownCategories.pickle'
            self.benchWords = self.mainBenchBase + 'brownWords.pickle'
            self.benchAmbiguousWords = self.mainBenchBase + 'brownAmbiguousWords.pickle'
            self.benchTrain =  self.mainBenchBase + 'brownAllPhrases.txt'
            self.benchError =  self.mainBenchBase + 'brownErrors.txt'
            
            self.baseRandBench = self.baseBench + 'randomTest/'
            self.benchRandWordsDico = self.baseRandBench + 'brownWordsDico.pickle'
            self.benchRandPosDico = self.baseRandBench + 'brownPosDico.pickle'
            self.benchRandMeta =  self.baseRandBench + 'metaData.txt'
            self.benchRandCategories = self.baseRandBench + 'categories.pickle'
            self.benchRandWords = self.baseRandBench + 'words.pickle'
            self.benchRandTrain =  self.baseRandBench + 'trainingPhrases.txt'
            self.benchRandTrainNotParsed =  self.baseRandBench + 'trainingPhrasesNotParsed.txt'
            self.benchRandTrainInd =  self.baseRandBench + 'trainingPhrases_ind.txt'
            self.benchRandTrainENNInd =  self.baseRandBench + 'trainingPhrasesENN_ind.txt'
            self.benchRandValidENNInd =  self.baseRandBench + 'validationPhrases_ind.txt'
            self.benchRandTest =  self.baseRandBench + 'testPhrases.txt'
            #self.benchRandTest =  self.baseRandBench + 'trainingPhrasesNotParsed.txt'
            self.benchRandTestParsed =  self.baseRandBench + 'testParsedPhrases.txt'            
            #self.benchRandTestParsed =  self.baseRandBench + 'trainingPhrases.txt'
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
        self.benchCrossTrainNotParsed =  self.baseCrossBenchSub + 'trainingPhrasesNotParsed.txt'
        self.benchCrossTrainInd =  self.baseCrossBenchSub + 'trainingPhrases_ind.txt'
        self.benchCrossTrainENNInd =  self.baseCrossBenchSub + 'trainingPhrasesENN_ind.txt'
        self.benchCrossValidENNInd =  self.baseCrossBenchSub + 'validationPhrases_ind.txt'
        self.benchCrossTest =  self.baseCrossBenchSub + 'testPhrases.txt'
        self.benchCrossTestParsed =  self.baseCrossBenchSub + 'testParsedPhrases.txt'
        self.benchCrossError =  self.baseCrossBenchSub + 'brownErrors.txt'
        
    
    def builfResultFile(self, model, crossNum=0, batch=True):
        
        if( model.lower() == 'blm'):
            self.benchTestBase = self.baseBench + 'testResult/blm/'
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            self.blmModelRandTagging =  self.benchTestBase + 'models/blmModelRandTagging.pickle'
            self.blmModelCrossTagging =  self.benchTestBase + 'models/blmModelCrossTagging_{0}.pickle'.format(crossNum)
            
        elif ( model.lower() == 'hmm'):
            self.benchTestBase = self.baseBench + 'testResult/hmm/'
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            self.hmmModelRandTagging =  self.benchTestBase + 'models/hmmModelRandTagging.pickle'
            self.hmmModelCrossTagging =  self.benchTestBase + 'models/hmmModelCrossTagging_{0}.pickle'.format(crossNum)
            
        elif ( model.lower() == 'hmm2'):
            self.benchTestBase = self.baseBench + 'testResult/hmm2/'
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            self.hmmModelRandTagging =  self.benchTestBase + 'models/hmmModelRandTagging.pickle'
            self.hmmModelCrossTagging =  self.benchTestBase + 'models/hmmModelCrossTagging_{0}.pickle'.format(crossNum)
            
        elif ( model.lower() == 'sechmm'):
            
            self.benchTestBase = self.baseBench + 'testResult/secoHmm/'
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            self.secHmmModelRandTagging =  self.benchTestBase + 'models/secHmmModelRandTagging.pickle'
            self.secHmmModelCrossTagging =  self.benchTestBase + 'models/secHmmModelCrossTagging_{0}.pickle'.format(crossNum)
        
        elif ( model.lower() == 'enn'):
            
            self.benchTestBase = self.baseBench + 'testResult/enn/'
           
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            
            if batch :
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennBatchModelRandTagging.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennBatchModelCrossTagging_{0}.pickle'.format(crossNum)
            else:
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennSeqModelRandTagging.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennSeqModelCrossTagging_{0}.pickle'.format(crossNum)
                
        elif ( model.lower() == 'enn2'):
            
            self.benchTestBase = self.baseBench + 'testResult/enn2/'
           
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            
            if batch :
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennBatchModelRandTagging.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennBatchModelCrossTagging_{0}.pickle'.format(crossNum)
            else:
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennSeqModelRandTagging.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennSeqModelCrossTagging_{0}.pickle'.format(crossNum)
        
        elif ( model.lower() == 'enn3'):
            
            self.benchTestBase = self.baseBench + 'testResult/enn3/'
           
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            
            if batch :
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennBatchModelRandTagging.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennBatchModelCrossTagging_{0}.pickle'.format(crossNum)
            else:
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennSeqModelRandTagging.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennSeqModelCrossTagging_{0}.pickle'.format(crossNum)
        
        elif ( model.lower() == 'enn4'):
            
            self.benchTestBase = self.baseBench + 'testResult/enn4/'
           
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            
            if batch :
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennBatchModelRandTagging.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennBatchModelCrossTagging_{0}.pickle'.format(crossNum)
            else:
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennSeqModelRandTagging.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennSeqModelCrossTagging_{0}.pickle'.format(crossNum)
                
        elif ( model.lower() == 'enn5'):
            
            self.benchTestBase = self.baseBench + 'testResult/enn5/'
           
            self.benchRandResultTagging =  self.benchTestBase + 'resultRandTagging_{0}_{1}.txt'
            self.benchCrossResultTagging =  self.benchTestBase + 'resultCrossTagging_{0}.txt'.format(crossNum)
            
            if batch :
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennBatchModelRandTagging_{0}_{1}.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennBatchModelCrossTagging_{0}.pickle'.format(crossNum)
            else:
                self.ennModelRandTagging =  self.benchTestBase + 'models/ennSeqModelRandTagging_{0}_{1}.pickle'
                self.ennModelCrossTagging =  self.benchTestBase + 'models/ennSeqModelCrossTagging_{0}.pickle'.format(crossNum)
        
        #print self.benchRandResultTagging
        #print self.benchCrossResultTagging        