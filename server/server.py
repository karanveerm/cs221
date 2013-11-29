from flask import Flask
from flask import url_for, redirect, request
import json
import inkml_to_pixels
import pickle 
import numpy as np
import itertools
import segment

app = Flask(__name__)

f = open('svm18px', 'r')
svm = pickle.load(f)
hmm_f = open('hmm18px', 'r')
hmm_instance = pickle.load(hmm_f)

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
  global svm
  strokes = json.loads(request.args.get('info'))
  symbolsIndices = segment.segmentSymbols(strokes)
  returnstr = ""
  for elem in symbolsIndices:
    s = [strokes[i] for i in elem]
    pixels = inkml_to_pixels.inkml_to_pixels(s)
    chain = list(itertools.chain(*pixels))
    chain.append(len(s))

    prediction = svm.predict(chain)[0]
    returnstr += prediction
  return returnstr

@app.route('/recognize-hmm', methods=['GET', 'POST'])
def recognize_hmm():
  global hmm_instance
  strokes = json.loads(request.args.get('info'))
  symbolsIndices = segment.segmentSymbols(strokes)
  returnstr = ""
  equation = []
  for elem in symbolsIndices:
    s = [strokes[i] for i in elem]
    pixels = inkml_to_pixels.inkml_to_pixels(s)
    chain = list(itertools.chain(*pixels))
    chain.append(len(s))
    equation.append((chain,))

  prediction = hmm_instance.compute_best_sequence(equation)
  for symbol in prediction:
    returnstr += symbol
  return returnstr

@app.route('/')
def home():
    return redirect(url_for('static', filename='character_recognizer.html'))

if __name__ == '__main__':
    app.run(debug=True)