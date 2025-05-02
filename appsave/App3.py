from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)#, static_url_path='/static')


if __name__ == '__main__':
    app.run(debug=True)
    
    
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
        return scaler.transform([[study_hours, prev_exam_score]])
    else:
        return np.array([[study_hours, prev_exam_score]])

# ... (rest of your code)

# Load the saved model
with open('model_pkl', 'rb') as f:
    model = pickle.load(f)

# Load the saved scaler
with open('scaler_pkl', 'rb') as f:
    scaler = pickle.load(f)

# Define a function for feature scaling
def scale_features(study_hours, prev_exam_score):
    return scaler.transform([[study_hours, prev_exam_score]])

# Define the route for rendering the HTML page
@app.route('/')
def index():
    return render_template('index.html')

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

        return jsonify({'result': result})

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'result': 'Error'})