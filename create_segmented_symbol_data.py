import os
import gettrace
import segment
import itertools
import inkml_to_pixels as itp
import pickle 

relative_path2011 = 'ICFHR_package/CROHME2011_data/CROHME_training/CROHME_training/'
relative_path2012 = 'ICFHR_package/CROHME2012_data/trainData/trainData/'

relative_testpath2011 = 'ICFHR_package/CROHME2011_data/CROHME_testGT/CROHME_testGT/'
relative_testpath2012 = 'ICFHR_package/CROHME2012_data/testDataGT/'

def getSegmentationAccuracy(pathArray):
  dataX = []
  dataY = []
  j = 0
  for path in pathArray:
    for f in os.listdir(path):
      j+=1
      if f[-5:] != "inkml": continue
      # print f
      traceList, symbolsList = gettrace.parseINKMLFile(path + f)
      segmentIndices = segment.segmentSymbols(traceList)
      for label, elem in symbolsList:
        # if label in ['=', 'i', 'j','\\leq', '\\log', '\\sin', '\\cos', '\\lim', '\\geq', '\\righarrow', '\\div']: continue
        
        # Correctly classified
        if elem in segmentIndices:
          strokes = [traceList[i] for i in elem]
          pixels = itp.inkml_to_pixels(strokes)
          chain = list(itertools.chain(*pixels))
          chain.append(len(strokes))
          dataX.append(chain)
          dataY.append(label)
          # cr.display(pixels)
      print j
  f = file("segmented_data_18", "w")
  pickle.dump((dataX, dataY), f)
if __name__ == "__main__":
  # getSegmentationAccuracy([relative_path2011, relative_path2012])
  getSegmentationAccuracy([relative_testpath2011, relative_testpath2012])
  # getSegmentationAccuracy([relative_testpath2012])