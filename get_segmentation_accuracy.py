import os
import gettrace
import segment

relative_path2011 = 'ICFHR_package/CROHME2011_data/CROHME_training/CROHME_training/'
relative_path2012 = 'ICFHR_package/CROHME2012_data/trainData/trainData/'

relative_testpath2011 = 'ICFHR_package/CROHME2011_data/CROHME_testGT/CROHME_testGT/'
relative_testpath2012 = 'ICFHR_package/CROHME2012_data/testDataGT/'

def getSegmentationAccuracy(pathArray):
  trainData = []
  from time import time
  start = time()
  completely_correct = 0
  total_files = 0
  correct = 0
  total = 0
  mistakes = {}
  numX = 0
  for path in pathArray:
    for file in os.listdir(path):
      if file[-5:] != "inkml": continue
      # print file
      traceList, symbolsList = gettrace.parseINKMLFile(path + file)
      segmentIndices = segment.segmentSymbols(traceList)
      correct_file = 0
      total_file = 0
      for label, elem in symbolsList:
        if label == "=" or label == 'i' or label =='j': continue
        if label == 'x': numX +=1
        if elem in segmentIndices:
          correct_file = correct_file + 1
        else:
          if label not in mistakes:
            mistakes[label] = 0
          mistakes[label] +=1
        total_file = total_file + 1

      if correct_file == total_file:
        completely_correct +=1

      correct += correct_file
      total += total_file

      total_files +=1
          # cr.display(pixels)
  print time()-start
  print float(correct)/total
  print float(completely_correct)/total_files
  print mistakes
  s = 0
  for elem in mistakes:
    s += mistakes[elem]
  print "sum is", s
  c = 0
  for elem in mistakes:
    c = c + mistakes[elem]
  print c
  print numX
if __name__ == "__main__":
  # getSegmentationAccuracy([relative_path2011, relative_path2012])
  getSegmentationAccuracy([relative_testpath2011, relative_testpath2012])
  # getSegmentationAccuracy([relative_testpath2012])