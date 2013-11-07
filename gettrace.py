from HTMLParser import HTMLParser
import segment

# create a subclass and override the handler methods
class MyINKMLParser(HTMLParser):
  def init(self):
    self.traceList = []
    self.index = -1
    self.inTrace = False

  def handle_starttag(self, tag, attrs):
    if tag.upper() == "TRACE":
      self.traceList.append([])
      self.index += 1
      self.inTrace = True

  def handle_endtag(self, tag):
    if tag.upper() == "TRACE":
      self.inTrace = False

  def handle_data(self, data):
    if self.inTrace:
      data = data.split(',')
      xy_pairs = [( float(elem.split()[0]), float(elem.split()[1])) for elem in data]
      self.traceList[self.index] = xy_pairs


# Given the path to an INKML file, this function will return a list where
# each element in the list corresponds to a trace.
# Each trace is represented as a list of (x,y) tuples.
def parseINKMLFile(filename):
  with file(filename) as f:
    s = f.read()
  parser = MyINKMLParser()
  parser.init()
  parser.feed(s)
  return parser.traceList


if __name__ == "__main__":
  # n = 'samples/test_sample_recognized.inkml'
  n = 'ICFHR_package/CROHME2012_data/testDataGT/001-equation003.inkml'
  # n = 'samples/train_sample_with_GT.inkml'
  traceList = parseINKMLFile(n)

  segmentIndices = segment.segmentSymbols(traceList)
