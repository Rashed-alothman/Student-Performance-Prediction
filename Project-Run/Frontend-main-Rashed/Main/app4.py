import logging
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd  # Add this import for DataFrame

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

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
        # Create a DataFrame with named columns
        input_data = pd.DataFrame({'Study Hours': [study_hours], 'Previous Exam Score': [prev_exam_score]})
        scaled_data = scaler.transform(input_data)
        
        # Return the scaled features without column names
        return scaled_data
    else:
        return np.array([[study_hours, prev_exam_score]])


# Define the route for rendering the HTML page
@app.route('/')
def index():
    return render_template('Project-Student-Exam-Performance-Prediction.html')

# Define the route for handling the prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from the request
        data = request.get_json()
        study_hours = float(data['studyHours'])
        prev_exam_score = float(data['prevExamScore'])

        # Scale input features
        scaled_features = scale_features(study_hours, prev_exam_score)

        # Perform the prediction using the loaded model
        result = model.predict(scaled_features)[0]
        
        # Map the numeric result to labels
        result_label = 'Pass' if result == 1 else 'Fail'

        return jsonify({'result': result_label})

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'result': 'Error'})

if __name__ == '__main__':
    app.run(debug=True)
# The app4.py script is similar to the app1.py script, but it includes the following changes: