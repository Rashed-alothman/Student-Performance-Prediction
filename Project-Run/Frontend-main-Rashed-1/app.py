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
#Project-Predict-Student-dropout-and-academic-success files are loaded
model_dropout = None
try:
    model_dropout = joblib.load('my_trained_model.joblib')
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")

#Project-Student-Exam-Performance-Prediction files 
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

#Project-Student-Performace
model_student_performance, scaler_student_performance = None, None
try:
    with open('model_pkl', 'rb') as f:
        model_student_performance = pickle.load(f)
    with open('scaler_pkl', 'rb') as f:
        scaler_student_performance = pickle.load(f)
        logging.info("Model and scaler are loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model or scaler: {e}")

def scale_features(study_hours, prev_exam_score):
    if scaler_student_performance is not None:
        # Create a DataFrame with named columns
        input_data = pd.DataFrame({'Study Hours': [study_hours], 'Previous Exam Score': [prev_exam_score]})
        scaled_data = scaler_student_performance.transform(input_data)
        
        # Return the scaled features without column names
        return scaled_data
    else:
        return np.array([[study_hours, prev_exam_score]])

# Define a function to check if the uploaded file has an allowed extension
def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# TODO Check if the student dropout is working or not 
@app.route('/Project-Run/Frontend-main-Rashed/Main/templates/Project-Student-dropout-and-academic-success.html', methods=['GET', 'POST'])
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

@app.route('/predict_csv', methods=['POST'])
def predict_csv():
    """Handle CSV file upload and prediction."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the file and make predictions
        return predict_from_csv(filepath)
    
# Define a function to process CSV file and predict
def predict_from_csv(filepath):
    # Read the CSV file without headers (header=None) and skip any initial space it is i FunctionIt will be added Later ##  header=None,
    df = pd.read_csv(filepath,  skipinitialspace=True)
    
    # Add column names to the dataframe
    column_names = ["Marital status", "Application mode", "Application order", "Course", "Daytime/evening attendance", "Previous qualification", "Nacionality", "Mother's qualification", "Father's qualification", "Mother's occupation", "Father's occupation", "Displaced", "Educational special needs", "Debtor", "Tuition fees up to date", "Gender", "Scholarship holder", "Age at enrollment", "International", "Curricular units 1st sem (credited)", "Curricular units 1st sem (enrolled)", "Curricular units 1st sem (evaluations)", "Curricular units 1st sem (approved)", "Curricular units 1st sem (grade)", "Curricular units 1st sem (without evaluations)", "Curricular units 2nd sem (credited)", "Curricular units 2nd sem (enrolled)", "Curricular units 2nd sem (evaluations)", "Curricular units 2nd sem (approved)", "Curricular units 2nd sem (grade)", "Curricular units 2nd sem (without evaluations)", "Unemployment rate", "Inflation rate", "GDP"]
    df.columns = column_names

    # If your model expects a specific number of columns, verify that here
    expected_num_columns = 34  
    # Change this to match your model's expected input
    if len(df.columns) != expected_num_columns:
        return jsonify({"error": f"Expected {expected_num_columns} columns, but got {len(df.columns)}"}), 430
    # predict and return the results.
    predictions = model_dropout.predict(df)
    return jsonify(predictions.tolist())

# define a function to proccess manual predictions
@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """Handle manual prediction requests."""
    if request.method == 'POST':
        data = request.get_json()
        df = pd.DataFrame([data])
        prediction = model_dropout.predict(df)
        return jsonify(prediction[0])
#----------------------------------------------------------------
# TODO Check if the student prediction is working or not
@app.route('/Project-Student-Exam-Performance-Prediction.html', methods=['GET', 'POST'])
def predict_exam_performance():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            study_hours = float(data['studyHours'])
            prev_exam_score = float(data['prevExamScore'])
            # Scale input features
            scaled_features = scale_features(study_hours, prev_exam_score)
            # Perform the prediction using the loaded model
            result = model_student_performance.predict(scaled_features)[0]
            # Map the numeric result to labels
            result_label = 'Pass' if result == 1 else 'Fail'
            return jsonify({'result': result_label})
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            return jsonify({'error': 'Failed to make prediction'}), 500
    return render_template('Project-Student-Exam-Performance-Prediction.html')

# ----------------------------------------------------------------
# TODO  Fix the student performance prediction

# Define the expected features for the model
EXPECTED_FEATURES = os.getenv('EXPECTED_FEATURES', [
    'sem_present_count', 'sem_absent_count', 'sem_eval_lec_test_1_mark',
    'sem_eval_lab_test_1_mark', 'semester_evaluation_mid_mark',
    'sem_eval_lec_test_2_mark', 'sem_eval_lab_test_2_mark',
    'semester_evaluation_pre_gtu_mark', 'semester_evaluation_internal_mark'
])
@app.route('/project-Student-Performace.html', methods=['GET', 'POST'])
def predict():
    """Predict the output based on the input data."""
    if request.method == 'POST':
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
    else:  # GET request
        # Dummy data for demonstration
        prediction = 85.0
        shap_values = [0.1, 0.2, 0.3, 0.4]
        return render_template('project-Student-Performace.html', prediction=prediction, shap_values=shap_values)

@app.route('/')
def main():
    return render_template('Main project.html')

@app.route('/Cards.html')
def cards():
    return render_template('Cards.html')

if __name__ == "__main__":
    app.run(debug=True)