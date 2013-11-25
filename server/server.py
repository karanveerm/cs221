from flask import Flask
from flask import url_for, redirect, request
import json
import inkml_to_pixel
from sklearn import linear_model, metrics
import pickle 
import numpy as np
from scipy import sparse

app = Flask(__name__)

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
  strokes = json.loads(request.args.get('info'))
  pixels = inkml_to_pixel.inkml_to_pixels(strokes)
  pixels = sum(pixels, [])
  pixels = np.array(pixels)
  
  print len(pixels)
  f = open("logreg", "r")
  lg = pickle.load(f)
  prediction = lg.predict(pixels)
  return prediction[0]
    
@app.route('/')
def home():
    return redirect(url_for('static', filename='character_recognizer.html'))

if __name__ == '__main__':
    app.run(debug=True)