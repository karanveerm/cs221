import os
import gettrace
import character_recognition as cr
relative_path = 'ICFHR_package/CROHME2012_data/trainData/trainData/'
trainData = []

def getTrainData(path):
  from time import time
  count = 0
  start = time()
  for file in os.listdir(path):
    if file[-5:] != "inkml": continue
    # print file
    traceList, symbolsList = gettrace.parseINKMLFile(path + file)
    for label, indices in symbolsList:
        pixels = cr.inkml_to_pixels([traceList[elem] for elem in indices])
        trainData.append((pixels, label))
        # cr.display(pixels)
  print time()-start
  print len(trainData)
  return trainData

if __name__ == "__main__":
  getTrainData(relative_path)