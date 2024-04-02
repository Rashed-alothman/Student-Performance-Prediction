from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import os
from joblib import load

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the trained model - replace with the path to your model
model_path = 'my_trained_model.joblib'
model = load(model_path)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file and make predictions
            return predict_from_csv(filepath)
    return render_template('index.html')

def predict_from_csv(filepath):
    """Function to process CSV file and predict."""
    df = pd.read_csv(filepath)
    # Assuming the model expects the same columns as in the CSV,
    # predict and return the results.
    predictions = model.predict(df)
    
    # For simplicity, returning the predictions as a string
    # Convert to appropriate response format as needed
    return jsonify(predictions.tolist())

@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """Handle manual prediction requests."""
    if request.method == 'POST':
        data = request.get_json()
        df = pd.DataFrame([data])
        prediction = model.predict(df)
        return jsonify(prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
