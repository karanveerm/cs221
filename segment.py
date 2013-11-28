import inkml_to_pixels as itp
import pickle
import itertools
import numpy as np
# 
# Given a traceList (list of strokes where each stroke is a list of (x,y) 
# tuples), it returns a list where each index corresponds to one or more strokes
# so that each index ends up corresponding to a symbol.
# eg. if it returns [[0], [1,2]], it means traceList[0] is one symbol and
# traceList[1] and traceList[2] together correspond to one symbol.
# 
# ASSUMPTIONS:
# * User writes from left to write and never goes back
# * If stroke i and stroke i+1 are parts of different symbols, then 
#   stroke i and stroke i+2 cannot be in the same symbol.
#
f = open('svm18px')
svm = pickle.load(f)
labels = svm.classes_

def segmentSymbols(traceList):
  symbol_index = 0
  symbol_trace_map = []
  # Add the first stroke
  symbol_trace_map.append([0])

  for i in range(1, len(traceList)):
    trace = traceList[i]
    distinct = True
    for prev_trace_index in symbol_trace_map[-1]:
      prev_trace = traceList[prev_trace_index]
      if tracesIntersect(prev_trace, trace):
      # if tracesIntersect(prev_trace, trace) or tracesIntersectProximity(prev_trace, trace):
        symbol_trace_map[-1].append(i)
        distinct = False
        break
    # If the symbols didn't intersect, previous symbol was only stroke, 
    # we check to see if the current symbol and new one make a special symbol like x
    if distinct and len(symbol_trace_map[-1]) == 1 and makeSpecialSymbol(traceList[symbol_trace_map[-1][-1]], trace):
      symbol_trace_map[-1].append(i)
    # We have a new symbol
    elif distinct:
      symbol_index += 1
      symbol_trace_map.append([i])

  # print symbol_trace_map
  return symbol_trace_map

def makeSpecialSymbol(prev_trace, trace):
  global svm
  global labels
  pixels = itp.inkml_to_pixels([prev_trace, trace])
  chain = list(itertools.chain(*pixels))
  chain.append(2)
  probabilities = svm.predict_proba(chain)
  probMax = np.amax(probabilities)
  indexOfMax = np.argmax(probabilities)
  if labels[indexOfMax] in ['x', 'k', '\\geq', 'i', 'j', '='] and probMax > 0.7: return True

  return False

# def tracesIntersectProximity(t1, t2):
#   def pointsProximity(p0, p1):
#     p0_x, p0_y = p0
#     p1_x, p1_y = p1
#     return abs(p1_x - p0_x)**2 + abs(p1_y - p0_y)**2

#   EPSILON = 10**-5
#   min_dist = float('inf')
#   for p1 in t1:
#     for p2 in t2:
#       dist = pointsProximity(p1, p2)
#       min_dist = dist if dist < min_dist else min_dist
#   return True if min_dist < EPSILON else False


def tracesIntersect(t1, t2):
  for i in range(len(t1) - 1):
    for j in range(len(t2) - 1):
      if linesIntersect(t1[i], t1[i + 1], t2[j], t2[j+1]): return True
  return False

# http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
def linesIntersect(p0, p1, p2, p3):
  p0_x, p0_y = p0
  p1_x, p1_y = p1
  p2_x, p2_y = p2
  p3_x, p3_y = p3
  
  s1_x = p1_x - p0_x;     
  s1_y = p1_y - p0_y;
  
  s2_x = p3_x - p2_x;     
  s2_y = p3_y - p2_y;

  denom = -s2_x * s1_y + s1_x * s2_y
  if denom == 0:
    # TODO: Lines could be collinear and not just parallel. Handle it.
    return False

  s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / denom;
  t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / denom;

  # Lines intersect
  if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
    return True

  return False