# app.py

from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load("trained_model.joblib")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the request
        data = request.json

        # Extract features from input data
        study_hours = data['Study Hours']
        prev_exam_score = data['Previous Exam Score']

        # Make predictions using the pre-trained model
        prediction = model.predict([[study_hours, prev_exam_score]])[0]
        predicted_result = 'Pass' if prediction == 1 else 'Fail'

        # Prepare response
        response = {'prediction': predicted_result}

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
