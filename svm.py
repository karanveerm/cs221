"""
http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC
"""

import pylab as pl
from sklearn import svm, metrics
import pickle

# Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.001)

# # This was originally used to pickle the SVM for HMMs:
# classifier = svm.SVC(gamma=0.001, probability=True)

f = open("characterdata24px", "r")
trainDataX, trainDataY, testDataX, testDataY = pickle.load(f)

classifier.fit(trainDataX, trainDataY)

# To pickle the SVM classifier
svm_f = open("svm24px", "w")
pickle.dump(classifier, svm_f)

expected = testDataY
predicted = classifier.predict(testDataX)

print classifier.score(testDataX, testDataY)

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))