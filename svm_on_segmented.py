import pickle

f = open("segmented_data_18", "r")          
testDataX, testDataY = pickle.load(f)

f = open('svm18px', "r")
svm = pickle.load(f)

predicted = svm.predict(testDataX)
print svm.score(testDataX, testDataY)