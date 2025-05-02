# Flask application
import logging
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__) # Initialize Flask application
logging.basicConfig(level=logging.DEBUG) # Setup basic logging

# Load the trained model and scaler from files
try:
    with open('best_rf_model.pkl', 'rb') as f: # Try to load the trained RandomForest model
        model = pickle.load(f)
except (EOFError, FileNotFoundError) as e: # If loading fails, log the error and set model to None
    logging.error(f'Error loading the model: {e}')
    model = None

# Load the saved scaler
try:
    with open('scaler.pkl', 'rb') as f: # Try to load the scaler used for feature scaling
        scaler = pickle.load(f)
except (EOFError, FileNotFoundError) as e: # If loading fails, log the error and set scaler to None
    logging.error(f'Error loading the scaler: {e}')
    scaler = None



# Try to load feature importances with error handling
try:
    with open('feature_importances.pkl', 'rb') as fi_file:
        feature_importances = pickle.load(fi_file)
except FileNotFoundError:
    logging.error('Feature importances file not found.')
except Exception as e:
    # Initialize an empty list or dict for feature importances as a fallback
    feature_importances = []
    logging.error(f'An error occurred while loading feature importances: {e}')

@app.route('/') # Home endpoint
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST']) # Prediction endpoint
def predict():
    # Check if model or scaler wasn't loaded correctly and return an error message
    if model is None or scaler is None:
        return jsonify({'error': 'Model or scaler is not loaded properly.'}), 500
    try:
        data = request.get_json() # Extract data from POST request
        
        # Assuming data is a dictionary with keys matching the feature names, minus the identifier and target
        # Convert input data to DataFrame to ensure compatibility with scaler and model
        input_features = pd.DataFrame([data])
        
        
        # Ensure the order of columns matches the training data
        # Define the expected features based on the model training
        expected_features = [
            'sem_present_count', 'sem_absent_count', 'sem_eval_lec_test_1_mark',
            'sem_eval_lab_test_1_mark', 'semester_evaluation_mid_mark',
            'sem_eval_lec_test_2_mark', 'sem_eval_lab_test_2_mark',
            'semester_evaluation_pre_gtu_mark', 'semester_evaluation_internal_mark'
        ]
        
        # Reorder or select the columns based on expected features
        input_features = input_features[expected_features] # Ensure DataFrame has the expected features
        
        # Scaling the input features
        input_scaled = scaler.transform(input_features) # Scale the input features
        
        # Predicting
        # Make prediction
        prediction = model.predict(input_scaled) # Predict using the model
        
        # Assuming the model returns a single value prediction
        # Return prediction in response
        return jsonify({'predicted_gtu_mark': prediction[0]})
    
    except Exception as e: # Handle exceptions
        logging.error(f'An error occurred during prediction: {e}')
        return jsonify({'error': str(e)})
    
@app.route('/feature_importances', methods=['GET'])
def get_feature_importances():
    # Check if feature importances data is available
    if not feature_importances:
        return jsonify({'error': 'Feature importances data is not available.'}), 404
    return jsonify(feature_importances) # Return the feature importances data
if __name__ == '__main__':
    app.run(debug=True) # Run the app in debug mode