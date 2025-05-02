# Standard library imports
import logging
import os
# Third party imports
from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import BadRequest
import pandas as pd
import numpy as np
import shap  # Assuming SHAP values are used for model explanations
import joblib



app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Define the expected features for the model
EXPECTED_FEATURES = os.getenv('EXPECTED_FEATURES', [
    'sem_present_count', 'sem_absent_count', 'sem_eval_lec_test_1_mark',
    'sem_eval_lab_test_1_mark', 'semester_evaluation_mid_mark',
    'sem_eval_lec_test_2_mark', 'sem_eval_lab_test_2_mark',
    'semester_evaluation_pre_gtu_mark', 'semester_evaluation_internal_mark'
])

# Initialize model, scaler, and explainer variables
model = scaler = explainer = None

def load_components()-> None:
    """Load model and explainer from joblib files."""
    global pipeline, explainer
    try:
        components = joblib.load('my_model.joblib')
        pipeline = components['pipeline']
        explainer = components['explainer']
        logging.info("Pipeline and explainer loaded successfully.")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except Exception as e:
        logging.error(f"Error loading components: {e}")

@app.route('/')
def index():
    # Serve the main page of the app
    return render_template('project-Student-Performace.html')

@app.route('/predict', methods=['POST'])
def predict() -> jsonify:
    """Predict the output based on the input data."""
    # Ensure the pipeline and explainer are loaded properly
    if not pipeline or not explainer:
        logging.error("Pipeline or explainer is not loaded properly.")
        return jsonify({'error': 'Pipeline or explainer is not loaded properly.'}), 500
    
    try:
        # Parse incoming request data
        data = request.get_json(force=True)
    except BadRequest:
        return jsonify({'error': 'Invalid JSON.'}), 400

    input_df = pd.DataFrame([data])

    # Check for missing expected features
    if not all(col in input_df.columns for col in EXPECTED_FEATURES):
        missing_cols = set(EXPECTED_FEATURES) - set(input_df.columns)
        logging.error(f"Missing columns in input data: {missing_cols}")
        return jsonify({'error': 'Missing required input features.', 'missing_features': list(missing_cols)}), 400

    try:
        # Make a prediction using the pipeline
        prediction = pipeline.predict(input_df[EXPECTED_FEATURES])[0]

        # Generate and format SHAP values for explanations
        shap_values = explainer.shap_values(input_df[EXPECTED_FEATURES])
        formatted_shap_values = shap_values[0].tolist() if isinstance(shap_values, list) else shap_values.tolist()

        #Return the prediction and SHAP values
        return jsonify({'predicted_gtu_mark': float(prediction), 'shap_values': formatted_shap_values})
    except Exception as e:
        logging.error(f"An error occurred during prediction: {e}")
        return jsonify({'error': 'Failed to make prediction'}), 500

if __name__ == '__main__':
    load_components()
    app.run(debug=os.getenv('DEBUG', 'True') == 'True')