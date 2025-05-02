# app.py
import joblib
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the saved model
try:
    with open('model_pkl', 'rb') as f:
        model = pickle.load(f)
except (EOFError, FileNotFoundError) as e:
    print(f'Error loading the model: {e}')
    model = None

# Load the saved scaler
try:
    with open('scaler_pkl', 'rb') as f:
        scaler = pickle.load(f)
except (EOFError, FileNotFoundError) as e:
    print(f'Error loading the scaler: {e}')
    scaler = None

# Define a function for feature scaling
def scale_features(study_hours, prev_exam_score):
    if scaler is not None:
        return scaler.transform([[study_hours, prev_exam_score]])
    else:
        return np.array([[study_hours, prev_exam_score]])

# ... (rest of your code)

# Load the pre-trained model
model = joblib.load("trained_model.joblib")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the request
        data = request.json

        # Extract features from input data
        study_hours = data['Study Hours']
        prev_exam_score = data['Previous Exam Score']

        # Make predictions using the pre-trained model
        prediction = model.predict([[study_hours, prev_exam_score]])[0]
        predicted_result = 'Pass' if prediction == 1 else 'Fail'

        # Prepare response
        response = {'prediction': predicted_result}

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
