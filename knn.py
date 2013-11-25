from sklearn import neighbors, metrics
import pickle

f = open("characterdata", "r")
trainDataX, trainDataY, testDataX, testDataY = pickle.load(f)

classifier = neighbors.KNeighborsClassifier()
classifier.fit(trainDataX, trainDataY)

print "Train accuracy is ", classifier.score(trainDataX, trainDataY)
print "Test accuracy is ", classifier.score(testDataX, testDataY)

expected = testDataY
predicted = classifier.predict(testDataX)

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))