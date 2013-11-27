import os
import gettrace
import itertools

relative_path2011 = 'ICFHR_package/CROHME2011_data/CROHME_training/CROHME_training/'
relative_path2012 = 'ICFHR_package/CROHME2012_data/trainData/trainData/'

relative_testpath2011 = 'ICFHR_package/CROHME2011_data/CROHME_testGT/CROHME_testGT/'
relative_testpath2012 = 'ICFHR_package/CROHME2012_data/testDataGT/'

# Returns a list of form [equation_1, equation_2, ...., equation_n] where
# equation_i is itself a list of the form ['a', '+', 'b', '=', 'c']
def getData(pathArray):
  equationData = []
  from time import time
  start = time()
  for path in pathArray:
    for file in os.listdir(path):
      if file[-5:] != "inkml": continue
      equationData.append(gettrace.parseSymbolOrder(path + file))
  print time()-start
  return equationData

def getTrainData():
  return getData([relative_path2011, relative_path2012])

def getTestData():
  return getData([relative_testpath2011, relative_testpath2012])
  
if __name__ == "__main__":
  # getData([relative_path2011, relative_path2012])
  getData([relative_testpath2011, relative_testpath2012])
