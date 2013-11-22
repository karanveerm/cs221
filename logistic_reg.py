"""
To learn how to get probability table for distribution etc
Use:
http://scikit-learn.sourceforge.net/dev/modules/generated/sklearn.linear_model.LogisticRegression.html
"""

from sklearn import linear_model, metrics
import pickle

f = open("characterdata", "r")
trainDataX, trainDataY, testDataX, testDataY = pickle.load(f)

lg = linear_model.LogisticRegression()
lg.fit(trainDataX, trainDataY)

print "Train accuracy is ", lg.score(trainDataX, trainDataY)
print "Test accuracy is ", lg.score(testDataX, testDataY)

expected = testDataY
predicted = lg.predict(testDataX)

print("Classification report for classifier %s:\n%s\n"
      % (lg, metrics.classification_report(expected, predicted)))