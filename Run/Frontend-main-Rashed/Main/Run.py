# Standard library imports
import os
import logging
import pickle
import numpy as np
import pandas as pd
import joblib

# Third party imports
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

# Flask app configuration
app = Flask(__name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# Load models and components
model_dropout = joblib.load('my_trained_model.joblib')
components = joblib.load('my_model.joblib')
pipeline = components['pipeline']
explainer = components['explainer']

model_student_performance, scaler_student_performance = None, None
try:
    with open('model_pkl', 'rb') as f:
        model_student_performance = pickle.load(f)
    with open('scaler_pkl', 'rb') as f:
        scaler_student_performance = pickle.load(f)
except Exception as e:
    logging.error(f"Error loading model or scaler: {e}")

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_from_csv(filepath):
    """Function to process CSV file and predict."""
    df = pd.read_csv(filepath, skipinitialspace=True)
    predictions = model_dropout.predict(df)
    return jsonify(predictions.tolist())

@app.route('/Project-Predict-Student-dropout-and-academic-success.html', methods=['GET', 'POST'])
def upload_dropout_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return predict_from_csv(filepath)
    return render_template('Project-Predict-Student-dropout-and-academic-success.html')

@app.route('/Project-Student-Exam-Performance-Prediction.html', methods=['GET', 'POST'])
def predict_exam_performance():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            input_df = pd.DataFrame([data])
            prediction = pipeline.predict(input_df)
            shap_values = explainer.shap_values(input_df)
            return jsonify({'predicted_gtu_mark': float(prediction[0]), 'shap_values': shap_values.tolist()})
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            return jsonify({'error': 'Failed to make prediction'}), 500
    return render_template('Project-Student-Exam-Performance-Prediction.html')

@app.route('/project-Student-Performace.html', methods=['GET', 'POST'])
def predict_student_performance():
    if request.method == 'POST':
        data = request.get_json()
        input_df = pd.DataFrame([data])
        if scaler_student_performance:
            scaled_features = scaler_student_performance.transform(input_df)
        else:
            scaled_features = input_df
        result = model_student_performance.predict(scaled_features)[0]
        result_label = 'Pass' if result == 1 else 'Fail'
        return jsonify({'result': result_label})
    return render_template('project-Student-Performace.html')

@app.route('/')
def main():
    return render_template('Main project.html')

@app.route('/Cards.html')
def cards():
    return render_template('Cards.html')

if __name__ == "__main__":
    app.run(debug=True)