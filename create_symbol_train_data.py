import os
import gettrace
import inkml_to_pixels as itp

relative_path2011 = 'ICFHR_package/CROHME2011_data/CROHME_training/CROHME_training/'
relative_path2012 = 'ICFHR_package/CROHME2012_data/trainData/trainData/'

relative_testpath2011 = 'ICFHR_package/CROHME2011_data/CROHME_testGT/CROHME_testGT/'
relative_testpath2012 = 'ICFHR_package/CROHME2012_data/testDataGT/'

def getTrainData(pathArray):
  trainData = []
  from time import time
  start = time()
  for path in pathArray:
    for file in os.listdir(path):
      if file[-5:] != "inkml": continue
      # print file
      traceList, symbolsList = gettrace.parseINKMLFile(path + file)
      for label, indices in symbolsList:
          pixels = itp.inkml_to_pixels([traceList[elem] for elem in indices])
          trainData.append((pixels, label))
          # itp.display(pixels)
  print time()-start
  print len(trainData)
  return trainData

if __name__ == "__main__":
  # getTrainData([relative_path2011, relative_path2012])
  getTrainData([relative_testpath2011, relative_testpath2012])