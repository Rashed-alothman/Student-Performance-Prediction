from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load pre-trained model
model = joblib.load("trained_model.joblib")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
    # Get input data from the request
        data = request.json

        # Extract features from input data (adjust according to your dataset)
        features = [data['Study Hours'], data['Previous Exam Score']]  # Adjust features based on your dataset

        # Make predictions using the pre-trained model
        prediction = model.predict([features])[0]

        # Prepare response
        response = {'prediction': prediction}

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
# app.py

#from flask import Flask, request, jsonify, render_template
#import joblib

#app = Flask(__name__)

# Load pre-trained model
#model = joblib.load("trained_model.joblib")

#@app.route('/')
#def index():
 #   return render_template('index.html')

#@app.route('/predict', methods=['POST'])
#def predict():
 #   try:
  #      # Get input data from the request
   #     data = request.json
#
 #       # Extract features from input data (adjust according to your dataset)
  #      features = [data['feature1'], data['feature2']]

        # Make predictions using the pre-trained model
   #     prediction = model.predict([features])[0]

        # Prepare response
    #    response = {'prediction': prediction}

     #   return jsonify(response)

    #except Exception as e:
     #   return jsonify({'error': str(e)})

#if __name__ == '__main__':
 #   app.run(debug=True)

# app.py