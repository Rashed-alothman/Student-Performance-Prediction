from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import os
import logging
from my_model_training import train_model  # This imports your model training function

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Assuming these are the features your model expects
EXPECTED_FEATURES = [...]

model, explainer = None, None

def load_or_train_components():
    """Load or train model and explainer."""
    global model, explainer
    try:
        # Attempt to load the model if it exists
        components = joblib.load('my_model.joblib')
        model = components['model']
        explainer = components['explainer']
        logging.info("Components loaded successfully.")
    except FileNotFoundError:
        # If not found, train the model
        logging.info("Model not found, training new model.")
        model, explainer = train_model()
        joblib.dump({'model': model, 'explainer': explainer}, 'my_model.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not explainer:
        return jsonify({'error': 'Model or explainer is not properly loaded'}), 500

    data = request.get_json(force=True)
    input_df = pd.DataFrame([data])
    
    if not all(col in input_df.columns for col in EXPECTED_FEATURES):
        missing_cols = set(EXPECTED_FEATURES) - set(input_df.columns)
        return jsonify({'error': 'Missing required input features.', 'missing_features': list(missing_cols)}), 400

    prediction = model.predict(input_df[EXPECTED_FEATURES])[0]
    shap_values = explainer.shap_values(input_df[EXPECTED_FEATURES])
    formatted_shap_values = shap_values[0].tolist() if isinstance(shap_values, list) else shap_values.tolist()

    return jsonify({'predicted_value': float(prediction), 'shap_values': formatted_shap_values})

if __name__ == '__main__':
    load_or_train_components()
    app.run(debug=True)
