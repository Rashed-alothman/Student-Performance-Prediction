import logging
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Load the saved model
try:
    with open('best_rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
except (EOFError, FileNotFoundError) as e:
    logging.error(f'Error loading the model: {e}')
    model = None

# Load the saved scaler
try:
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
except (EOFError, FileNotFoundError) as e:
    logging.error(f'Error loading the scaler: {e}')
    scaler = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from the request
        data = request.get_json()
        
        # Define the feature names based on your training data
        feature_names = [
            'sem_present_count', 'sem_absent_count', 'sem_eval_lec_test_1_mark',
            'sem_eval_lab_test_1_mark', 'semester_evaluation_mid_mark',
            'sem_eval_lec_test_2_mark', 'sem_eval_lab_test_2_mark',
            'semester_evaluation_pre_gtu_mark', 'semester_evaluation_internal_mark'
        ]
        
        # Create a DataFrame for the input features
        input_features = pd.DataFrame([data], columns=feature_names)
        
        # Scale input features
        scaled_features = scaler.transform(input_features)

        # Perform the prediction using the loaded model
        prediction = model.predict(scaled_features)[0]

        # Construct a response dictionary
        response = {'predicted_final_exam_marks': float(prediction)}

        return jsonify(response)

    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
