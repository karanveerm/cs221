import create_equation_unary_data as ceud
import pickle

data = ceud.getTestData()

f = open('svm18px', "r")
svm = pickle.load(f)


total = 0
total_correct = 0
off_by_one = 0
off_by_two = 0

for equation in data:
  correct = 0
  for pixel_array, label in equation:
    if svm.predict(pixel_array)[0] == label:
      correct +=1
  if correct == len(equation):
    total_correct +=1
  if correct + 1 >= len(equation):
    off_by_one +=1
  if correct + 2 >= len(equation):
    off_by_two +=1
  total +=1

print total_correct
print off_by_one
print off_by_two

print total
print float(total_correct)/total
print float(off_by_one)/total
print float(off_by_two)/total