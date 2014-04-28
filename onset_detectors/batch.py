#!/usr/bin/env python
import sys, shutil, os

import glob
import shutil
import onset_evaluation
import StringIO
import csv

#Helper function to move all files by type
def copyFilesByType(source, destination, extension):
    for path in glob.glob(source + "/*." + extension):
        shutil.copy(path, destination)


moduleNames = ['SuperFlux', 'essentia_global', 'essentia_example', 'modal_batch']
#moduleNames = ['SuperFlux']
modules = map(__import__, moduleNames)

scriptRoot='/Users/carthach/Dev/mtg/my_projects/onset_detection/Onset-Standalone-References/onset_detectors'
datasetRoot = '/Users/carthach/GiantSteps-Share/datasets/'

datasets = {
   "ENST-1":{
          "audio":"ENST/drummer_1/audio",
          "annotations":"ENST/drummer_1/annotation"
          },

   "ENST-2":{
          "audio":"ENST/drummer_2/audio",
          "annotations":"ENST/drummer_2/annotation"
          },

   "ENST-3":{
          "audio":"ENST/drummer_3/audio",
          "annotations":"ENST/drummer_3/annotation"
          },

    "JKU":{
           "audio":"jku/onsets/audio/",
           "annotations":"jku/onsets/annotations/onsets/"
           },

    "Modal":{
           "audio":"Modal/audio/",
           "annotations":"Modal/annotations/"
           },
}

# datasets = {
#    "ENST-1":{
#           "audio":"ENST/drummer_1/audio",
#           "annotations":"ENST/drummer_1/annotation"
#           },

#    "ENST-2":{
#           "audio":"ENST/drummer_2/audio",
#           "annotations":"ENST/drummer_2/annotation"
#           },

# }

outputRoot = '/Users/carthach/Dev/mtg/my_projects/onset_detection/Onset-Standalone-References/eval'

overallResults = {}
datasetResults = {}

for module in modules:
    moduleName = module.__name__
    scriptFilename = moduleName + '.py'

    print 'Current Script: ' + moduleName
    for datasetName  in datasets:
        print '    Dataset: ' + datasetName
        datasetAudioPath = datasetRoot + datasets[datasetName]['audio']

        outputPath = outputRoot + '/' + module.__name__ + '/' + datasetName
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        
        sys.argv = [module.__file__, datasetAudioPath]
        module.main()
        
        copyFilesByType(datasetAudioPath, outputPath, 'txt')

        #Now let's compare to datasetGTPath
        datasetGroundTruthPath = datasetRoot + datasets[datasetName]['annotations']

        outputEvalName = moduleName + '_' + datasetName + '.txt'
        sys.stdout = mystdout = StringIO.StringIO()

        sys.argv = [onset_evaluation.__file__, outputPath, datasetGroundTruthPath]
        out = onset_evaluation.main()

        results = mystdout.getvalue()
        resultsAsFile = StringIO.StringIO(results)
        
        csv_values = csv.DictReader(resultsAsFile)

        #Reset stdout
        sys.stdout = sys.__stdout__

        # for num, line in enumerate(csv_values):
        #     if num == 0:
        #         datasetResults[moduleName] = {}
        #         datasetResults[moduleName][datasetName] = line
        #         break

        
        if not overallResults.get(moduleName):
            overallResults[moduleName] = out
        else:        
            x = overallResults[moduleName]
            y = out

            overallResults[moduleName] = {k: x.get(k,0) + y.get(k,0) for k in set(x) & set(y)}

noOfDatasets = len(datasets)
for module in modules:
    moduleName = module.__name__
    x = overallResults[moduleName]
    overallResults[moduleName] = {k: x.get(k,0) / noOfDatasets for k in set(x)}

print overallResults

        
