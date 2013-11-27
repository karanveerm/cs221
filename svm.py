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

f = open("characterdata", "r")
trainDataX, trainDataY, testDataX, testDataY = pickle.load(f)

classifier.fit(trainDataX, trainDataY)

# # To pickle the SVM classifier
# svm_f = open("svm", "w")
# pickle.dump(classifier, svm_f)

expected = testDataY
predicted = classifier.predict(testDataX)

print classifier.score(testDataX, testDataY)

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))

"""
0.646488604723
/Users/karanveer/anaconda/lib/python2.7/site-packages/sklearn/metrics/metrics.py:1905: UserWarning: The sum of true positives and false positives are equal to zero for some labels. Precision is ill defined for those labels [',' '.' '/' '7' 'A' 'B' 'X' 'Y' '[' '\\div' '\\exists' '\\forall'
 '\\gamma' '\\geq' '\\gt' '\\in' '\\int' '\\ldots' '\\leq' '\\lt' '\\neq'
 '\\phi' '\\pi' '\\pm' '\\sum' '\\{' '\\}' ']' 'f' 'g' 'j' 'm' 'p' 'r' 't']. The precision and recall are equal to zero for some labels. fbeta_score is ill defined for those labels ['!' ',' '.' '/' '7' 'A' 'B' 'X' 'Y' '[' '\\div' '\\exists' '\\forall'
 '\\gamma' '\\geq' '\\gt' '\\in' '\\int' '\\ldots' '\\leq' '\\lt' '\\neq'
 '\\phi' '\\pi' '\\pm' '\\sum' '\\times' '\\{' '\\}' ']' 'f' 'g' 'j' 'm'
 'p' 'r' 't']. 
  average=None)
Classification report for classifier SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
  gamma=0.001, kernel=rbf, max_iter=-1, probability=False,
  random_state=None, shrinking=True, tol=0.001, verbose=False):
             precision    recall  f1-score   support

          !       0.00      0.00      0.00        15
          (       0.83      0.84      0.84       605
          )       0.79      0.84      0.81       605
          +       0.52      0.97      0.67       683
          ,       0.00      0.00      0.00        62
          -       0.89      1.00      0.94       922
          .       0.00      0.00      0.00         8
          /       0.00      0.00      0.00        15
          0       0.60      0.82      0.69       185
          1       0.51      0.53      0.52       729
          2       0.56      0.83      0.67       893
          3       0.51      0.53      0.52       236
          4       0.44      0.55      0.49       151
          5       1.00      0.03      0.06        95
          6       0.40      0.24      0.30        67
          7       0.00      0.00      0.00        82
          8       0.58      0.11      0.18        64
          9       0.67      0.26      0.38        76
          =       0.75      0.70      0.73       402
          A       0.00      0.00      0.00        28
          B       0.00      0.00      0.00        24
          C       0.14      0.27      0.19        22
          F       1.00      0.17      0.29        12
          X       0.00      0.00      0.00        14
          Y       0.00      0.00      0.00         5
          [       0.00      0.00      0.00        14
     \alpha       0.65      0.60      0.62        99
      \beta       0.56      0.59      0.57        49
       \cos       0.88      0.88      0.88       122
       \div       0.00      0.00      0.00        14
    \exists       0.00      0.00      0.00         3
    \forall       0.00      0.00      0.00        10
     \gamma       0.00      0.00      0.00         7
       \geq       0.00      0.00      0.00        26
        \gt       0.00      0.00      0.00         6
        \in       0.00      0.00      0.00         7
     \infty       0.71      0.18      0.29        28
       \int       0.00      0.00      0.00        35
     \ldots       0.00      0.00      0.00        10
       \leq       0.00      0.00      0.00        32
       \lim       0.75      0.08      0.15        73
       \log       0.86      0.83      0.84        23
        \lt       0.00      0.00      0.00        13
       \neq       0.00      0.00      0.00        17
       \phi       0.00      0.00      0.00        11
        \pi       0.00      0.00      0.00        64
        \pm       0.00      0.00      0.00        16
\rightarrow       0.84      0.37      0.51        73
       \sin       0.85      0.74      0.79       141
      \sqrt       0.87      0.77      0.82       135
       \sum       0.00      0.00      0.00        47
       \tan       0.10      0.80      0.18         5
     \theta       0.43      0.14      0.21        21
     \times       0.00      0.00      0.00        48
         \{       0.00      0.00      0.00        12
         \}       0.00      0.00      0.00        12
          ]       0.00      0.00      0.00        14
          a       0.72      0.66      0.69       293
          b       0.68      0.61      0.65       201
          c       0.74      0.16      0.26       107
          d       0.73      0.68      0.71       111
          e       0.93      0.30      0.46       129
          f       0.00      0.00      0.00        28
          g       0.00      0.00      0.00        10
          i       0.62      0.05      0.08       111
          j       0.00      0.00      0.00        10
          k       1.00      0.15      0.25       137
          m       0.00      0.00      0.00        10
          n       0.68      0.56      0.61       264
          p       0.00      0.00      0.00        16
          r       0.00      0.00      0.00        13
          t       0.00      0.00      0.00        73
          x       0.53      0.86      0.66       681
          y       0.78      0.67      0.72       216
          z       0.30      0.24      0.27       100

avg / total       0.62      0.65      0.60      9697
"""