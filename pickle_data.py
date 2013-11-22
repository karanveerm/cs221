import numpy as np
from scipy import sparse
import create_symbol_data as c
import pickle

trainDataX, trainDataY = c.getData([c.relative_path2011, c.relative_path2012])
testDataX, testDataY = c.getData([c.relative_testpath2011, c.relative_testpath2012])

trainDataX = np.array(trainDataX)
trainDataX = sparse.csr_matrix(trainDataX)
testDataX = np.array(testDataX)
testDataX = sparse.csr_matrix(testDataX)
f = file("characterdata", "w")          
pickle.dump((trainDataX, trainDataY, testDataX, testDataY), f)