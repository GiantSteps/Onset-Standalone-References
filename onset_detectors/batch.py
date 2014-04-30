#!/usr/bin/env python
import sys, shutil, os

import glob
import shutil
import onset_evaluation
import StringIO
import csv
import xlsxwriter

#Helper function to move all files by type
def copyFilesByType(source, destination, extension):
    for path in glob.glob(source + "/*." + extension):
        shutil.copy(path, destination)

'''
Add algorithms as modules here
''' 

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

csvResults = {}

#Create Excel spreadsheet
workbook = xlsxwriter.Workbook(outputRoot + '/results.xlsx')
worksheet1 = workbook.add_worksheet('Overall')
bold = workbook.add_format({'bold': True})

noOfDatasets = len(datasets)

#Loop through every algorithm
for module in modules:
    moduleName = module.__name__
    scriptFilename = moduleName + '.py'

    #Create a worksheet for every algorithm
    currentWorksheet = workbook.add_worksheet(moduleName)
    row = 0
    currentWorksheet.write(row, 0, 'Dataset', bold)
    currentWorksheet.write(row, 1, 'Files', bold)
    currentWorksheet.write(row, 2, 'Onsets', bold)
    currentWorksheet.write(row, 3, 'Precision', bold)
    currentWorksheet.write(row, 4, 'Recall', bold)
    currentWorksheet.write(row, 5, 'F-Measure', bold)
#    currentWorksheet.write(row, 6, 'TP', bold)
#    currentWorksheet.write(row, 7, 'FP', bold)
#    currentWorksheet.write(row, 8, 'FN', bold)

    print 'Current Script: ' + moduleName

    #Loop through every dataset
    for datasetName  in datasets:
        row = row + 1

        print '    Dataset: ' + datasetName
        datasetAudioPath = datasetRoot + datasets[datasetName]['audio']

        #Where to dump our analyses
        outputPath = outputRoot + '/' + module.__name__ + '/' + datasetName
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        
        #SET SYS ARGV then run the algorithms  
        sys.argv = [module.__file__, datasetAudioPath]
        module.main()
        
        copyFilesByType(datasetAudioPath, outputPath, 'txt')

        datasetGroundTruthPath = datasetRoot + datasets[datasetName]['annotations']

        outputEvalName = moduleName + '_' + datasetName + '.txt'

        sys.argv = [onset_evaluation.__file__, outputPath, datasetGroundTruthPath]
        out = onset_evaluation.main()

        currentWorksheet.write(row, 0, datasetName, bold)
        currentWorksheet.write(row, 1, out['files'])
        currentWorksheet.write(row, 2, out['targets'])
        currentWorksheet.write(row, 3, out['p'])
        currentWorksheet.write(row, 4, out['r'])
        currentWorksheet.write(row, 5, out['f'])
#        currentWorksheet.write(row, 6, out['tp'])
#        currentWorksheet.write(row, 7, out['fp'])
#        currentWorksheet.write(row, 8, out['fn'])

        #Reset stdout
        sys.stdout = sys.__stdout__
        
        if not csvResults.get(moduleName):
            csvResults[moduleName] = out
        else:        
            x = csvResults[moduleName]
            y = out

            csvResults[moduleName] = {k: x.get(k,0) + y.get(k,0) for k in set(x) & set(y)}

    
    row = row + 1
    currentWorksheet.write(row, 0, 'TOTAL/AVERAGE', bold)
    currentWorksheet.write(row, 1, '=SUM(B2:B' + str(noOfDatasets+1) + ')')
    currentWorksheet.write(row, 2, '=SUM(C2:C' + str(noOfDatasets+1) + ')')
    currentWorksheet.write(row, 3, '=AVERAGE(D2:D' + str(noOfDatasets+1) + ')')
    currentWorksheet.write(row, 4, '=AVERAGE(E2:E' + str(noOfDatasets+1) + ')')
    currentWorksheet.write(row, 5, '=AVERAGE(F2:F' + str(noOfDatasets+1) + ')')
#    currentWorksheet.write(row, 6, '=SUM(G2:G' + str(noOfDatasets+1) + ')')
#    currentWorksheet.write(row, 7, '=SUM(H2:H' + str(noOfDatasets+1) + ')')
#    currentWorksheet.write(row, 8, '=SUM(I2:I' + str(noOfDatasets+1) + ')')

#Print a CSV summary as well
csvFileName = outputRoot + '/results.csv'
csvFile = open(csvFileName, 'w')
csvFile.write('Algorithm, Precision, Recall, F-Measure\n')

#Headers for the main sheet
row = 0
worksheet1.write(row, 0, 'Algorithm', bold)
worksheet1.write(row, 1, 'Precision', bold)
worksheet1.write(row, 2, 'Recall', bold)
worksheet1.write(row, 3, 'F-Measure', bold)

# worksheet1.write(row, 5, 'Algorithm Details', bold)
# worksheet1.write(row, 6, 'Window Type', bold)
# worksheet1.write(row, 7, 'Frame Size', bold)
# worksheet1.write(row, 8, 'Hop Size', bold)

for module in modules:
    moduleName = module.__name__

    row = row + 1
    x = csvResults[moduleName]
    
    csvResults[moduleName] = {k: x.get(k,0) / noOfDatasets for k in set(x)}

    outputString = moduleName + ',' + str(csvResults[moduleName]['p']) + ',' + str(csvResults[moduleName]['r']) + ',' + str(csvResults[moduleName]['f']) + '\n'
    csvFile.write(outputString)

    worksheet1.write(row,0,moduleName, bold)

    #Get Average P/R/F here and put on main sheet

    queryString = "='" + moduleName + "'" + '!' + 'D' + str(noOfDatasets+2)
    worksheet1.write(row,1,queryString)

    queryString = "='" + moduleName + "'" + '!' + 'E' + str(noOfDatasets+2)
    worksheet1.write(row,2,queryString)

    queryString = "='" + moduleName + "'" + '!' + 'F' + str(noOfDatasets+2)
    worksheet1.write(row,3,queryString)


#Print some Overall info



workbook.close()
csvFile.close()
