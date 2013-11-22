import os
import gettrace
import itertools
import inkml_to_pixels as itp

relative_path2011 = 'ICFHR_package/CROHME2011_data/CROHME_training/CROHME_training/'
relative_path2012 = 'ICFHR_package/CROHME2012_data/trainData/trainData/'

relative_testpath2011 = 'ICFHR_package/CROHME2011_data/CROHME_testGT/CROHME_testGT/'
relative_testpath2012 = 'ICFHR_package/CROHME2012_data/testDataGT/'

def getData(pathArray):
  dataX = []
  dataY = []
  from time import time
  start = time()
  for path in pathArray:
    for file in os.listdir(path):
      if file[-5:] != "inkml": continue
      traceList, symbolsList = gettrace.parseINKMLFile(path + file)
      for label, indices in symbolsList:
          pixels = itp.inkml_to_pixels([traceList[elem] for elem in indices])
          chain = list(itertools.chain(*pixels))
          dataX.append(chain)
          dataY.append(label)
          # itp.display(pixels)
  print time()-start
  return dataX, dataY

if __name__ == "__main__":
  # getData([relative_path2011, relative_path2012])
  getData([relative_testpath2011, relative_testpath2012])
