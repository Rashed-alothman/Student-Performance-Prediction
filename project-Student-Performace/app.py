from flask import Flask, render_template, request, jsonify
import logging
import pickle
import pandas as pd
import numpy as np
import shap  # Assuming SHAP values are used for model explanations

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the expected features for the model
expected_features = [
    'sem_present_count', 'sem_absent_count', 'sem_eval_lec_test_1_mark',
    'sem_eval_lab_test_1_mark', 'semester_evaluation_mid_mark',
    'sem_eval_lec_test_2_mark', 'sem_eval_lab_test_2_mark',
    'semester_evaluation_pre_gtu_mark', 'semester_evaluation_internal_mark'
]

# Initialize model, scaler, and explainer variables
model = scaler = explainer = None

# Safe loading of model, scaler, and SHAP explainer
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('shap_explainer.pkl', 'rb') as f:
        explainer = pickle.load(f)
    logging.info("Model, scaler, and SHAP explainer loaded successfully.")
except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
except Exception as e:
    logging.error(f"Error loading components: {e}")

@app.route('/')
def index():
    # Serve the main page of the app
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Ensure the model and scaler are loaded properly
    if not model or not scaler or not explainer:
        logging.error("Model, scaler, or explainer is not loaded properly.")
        return jsonify({'error': 'Model, scaler, or explainer is not loaded properly.'}), 500
    
    # Parse incoming request data
    data = request.get_json(force=True)
    input_df = pd.DataFrame([data])

    # Check for missing expected features
    if not all(col in input_df.columns for col in expected_features):
        missing_cols = set(expected_features) - set(input_df.columns)
        logging.error(f"Missing columns in input data: {missing_cols}")
        return jsonify({'error': 'Missing required input features.', 'missing_features': list(missing_cols)}), 400

    try:
        # Scale input data and make a prediction
        input_scaled = scaler.transform(input_df[expected_features])
        prediction = model.predict(input_scaled)[0]

        # Generate and format SHAP values for explanations
        shap_values = explainer.shap_values(input_scaled)
        formatted_shap_values = shap_values[0].tolist() if isinstance(shap_values, list) else shap_values.tolist()

        # Return the prediction and SHAP values
        return jsonify({'predicted_gtu_mark': float(prediction), 'shap_values': formatted_shap_values})
    except Exception as e:
        logging.error(f"An error occurred during prediction: {e}")
        return jsonify({'error': 'Failed to make prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True)
