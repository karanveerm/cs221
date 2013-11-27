from HTMLParser import HTMLParser
import segment

# create a subclass and override the handler methods
class MyINKMLParser(HTMLParser):
  def init(self):
    self.traceList = []
    self.symbolsList = []
    self.symbolOrder = {}
    self.currSymbol = None
    self.symbolIndex = -1
    self.traceIndex = -1
    self.inTrace = False
    self.inAnnotation = False
    self.inSegmentation = False
    self.inSymbolInfo = False
    self.symbolName = False

  def handle_starttag(self, tag, attrs):
    if tag.upper() == "TRACE":
      self.traceList.append([])
      self.traceIndex += 1
      self.inTrace = True
    elif tag.upper() == "ANNOTATION" and not self.inSymbolInfo:
      self.inAnnotation = True
    elif tag.upper() == "TRACEGROUP" and self.inSegmentation:
      self.inSymbolInfo = True
    elif tag.upper() == "ANNOTATION" and self.inSymbolInfo:
      self.symbolName = True
    elif tag.upper() == "TRACEVIEW":
      strokeNum = int(attrs[0][1])
      if self.currSymbol != None:
        self.symbolOrder[strokeNum] = self.currSymbol
        self.currSymbol = None
      self.symbolsList[self.symbolIndex][1].append(strokeNum)

  def handle_endtag(self, tag):
    if tag.upper() == "TRACE":
      self.inTrace = False
    elif tag.upper() == "ANNOTATION":
      self.inAnnotation = False
    elif tag.upper() == "TRACEGROUP" and self.inSegmentation:
      self.inSymbolInfo = False

  def handle_data(self, data):
    if self.inTrace:
      data = data.split(',')
      xy_pairs = [( float(elem.split()[0]), float(elem.split()[1])) for elem in data]
      self.traceList[self.traceIndex] = xy_pairs
    if self.inAnnotation:
      if data=="Segmentation":
        self.inSegmentation = True
    if self.symbolName:
      self.symbolIndex +=1
      self.symbolsList.append((data,[]))
      self.currSymbol = data
      self.symbolName = False

# Given the path to an INKML file, this function will return a list where
# each element in the list corresponds to a trace.
# Each trace is represented as a list of (x,y) tuples.
def parseINKMLFile(filename):
  with file(filename) as f:
    s = f.read()
  parser = MyINKMLParser()
  parser.init()
  parser.feed(s)  
  return parser.traceList, parser.symbolsList

# Given the path to an INKML file, 
def parseSymbolOrder(filename):
  orderedSymbolList = []
  with file(filename) as f:
    s = f.read()
  parser = MyINKMLParser()
  parser.init()
  parser.feed(s) 
  for key in sorted(parser.symbolOrder):
    orderedSymbolList.append(parser.symbolOrder[key])
  return orderedSymbolList

if __name__ == "__main__":
  # n = 'samples/test_sample_recognized.inkml'
  # n = 'ICFHR_package/CROHME2012_data/testDataGT/001-equation001.inkml'
  n = 'ICFHR_package/CROHME2012_data/trainData/trainData/algb09.inkml'
  # n = 'samples/train_sample_with_GT.inkml'
  traceList, symbolsList = parseINKMLFile(n)

  segmentIndices = segment.segmentSymbols(traceList)
