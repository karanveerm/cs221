import os
import gettrace
import itertools
import inkml_to_pixels as itp

relative_path2011 = 'ICFHR_package/CROHME2011_data/CROHME_training/CROHME_training/'
relative_path2012 = 'ICFHR_package/CROHME2012_data/trainData/trainData/'

relative_testpath2011 = 'ICFHR_package/CROHME2011_data/CROHME_testGT/CROHME_testGT/'
relative_testpath2012 = 'ICFHR_package/CROHME2012_data/testDataGT/'

# Returns:
# List of [equation_1, equation_2..... equation_n]
# where equation_i  = list of (vectorized_pixel_array, label) for each symbol in equation_i

def getData(pathArray):
  data = []
  from time import time
  start = time()
  for path in pathArray:
    for file in os.listdir(path):
      if file[-5:] != "inkml": continue
      traceList, symbolsList = gettrace.parseINKMLFile(path + file)
      equationDict = {}
      for label, indices in symbolsList:
          strokes = [traceList[elem] for elem in indices]
          pixels = itp.inkml_to_pixels(strokes)
          chain = list(itertools.chain(*pixels))
          chain.append(len(strokes))
          equationDict[indices[0]] = (chain, label)
      equationList = []
      for key in sorted(equationDict):
        equationList.append(equationDict[key])
      data.append(equationList)
          # itp.display(pixels)
  print time()-start
  return data

def getTrainData():
  return getData([relative_path2011, relative_path2012])

def getTestData():
  return getData([relative_testpath2011, relative_testpath2012])

if __name__ == "__main__":
  # getData([relative_path2011, relative_path2012])
  getData([relative_testpath2011, relative_testpath2012])
