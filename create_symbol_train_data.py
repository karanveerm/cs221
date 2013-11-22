import os
import gettrace
import character_recognition as cr
import itertools

relative_path2011 = 'ICFHR_package/CROHME2011_data/CROHME_training/CROHME_training/'
relative_path2012 = 'ICFHR_package/CROHME2012_data/trainData/trainData/'

relative_testpath2011 = 'ICFHR_package/CROHME2011_data/CROHME_testGT/CROHME_testGT/'
relative_testpath2012 = 'ICFHR_package/CROHME2012_data/testDataGT/'

def getTrainData(pathArray):
  trainDataX = []
  trainDataY = []
  from time import time
  start = time()
  for path in pathArray:
    for file in os.listdir(path):
      if file[-5:] != "inkml": continue
      traceList, symbolsList = gettrace.parseINKMLFile(path + file)
      for label, indices in symbolsList:
          pixels = cr.inkml_to_pixels([traceList[elem] for elem in indices])
          chain = list(itertools.chain(*pixels))
          trainDataX.append(chain)
          trainDataY.append(label)
          # cr.display(pixels)
  print time()-start
  return trainDataX, trainDataY

if __name__ == "__main__":
  # getTrainData([relative_path2011, relative_path2012])
  getTrainData([relative_testpath2011, relative_testpath2012])