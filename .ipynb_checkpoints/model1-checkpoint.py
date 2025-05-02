# model.py

from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd

def train_model_and_save(data):
    # Extract features and target variable from the data
    features = data[['Study Hours', 'Previous Exam Score']]
    target = data['Pass/Fail']

    # Train the logistic regression model
    model = LogisticRegression()
    model.fit(features, target)

    # Save the trained model
    joblib.dump(model, 'trained_model.joblib')

if __name__ == '__main__':
    # Load your training data from a CSV file
    training_data = pd.read_csv('student_exam_data.csv')

    # Train the model and save it
    train_model_and_save(training_data)
