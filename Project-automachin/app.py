from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import logging
import pickle
import pandas as pd
import numpy as np
import shap

app = Flask(__name__)
socketio = SocketIO(app)
logging.basicConfig(level=logging.INFO)

# Load the machine learning components
try:
    with open('automl_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('shap_explainer.pkl', 'rb') as f:
        explainer = pickle.load(f)
except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
    model, scaler, explainer = None, None, None
except Exception as e:
    logging.error(f"Error loading components: {e}")
    model, scaler, explainer = None, None, None

@app.route('/')
def index():
    # Serve the main page of the app
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Endpoint for generating predictions and explanations
    if model is None or scaler is None or explainer is None:
        return jsonify({'error': 'Model, scaler, or explainer is not loaded properly.'}), 500
    
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data])
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        
        # Generate SHAP values for the input data for explanations
        shap_values = explainer.shap_values(input_scaled)
        
        # Convert SHAP values to a format that can be easily sent as JSON
        shap_values_json = shap_values[0].tolist() if isinstance(shap_values, list) else shap_values.tolist()
        
        return jsonify({'predicted_gtu_mark': float(prediction), 'shap_values': shap_values_json})
    except Exception as e:
        app.logger.error(f'An error occurred during prediction: {e}')
        return jsonify({'error': 'Failed to make prediction'}), 500

# SocketIO events
@socketio.on('connect')
def test_connect():
    emit('after connect', {'data':'Let\'s dance'})

if __name__ == '__main__':
    socketio.run(app, debug=True)