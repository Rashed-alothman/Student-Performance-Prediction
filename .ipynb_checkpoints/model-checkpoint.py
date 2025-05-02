# model.py

from sklearn.linear_model import LinearRegression
import joblib
import pandas as pd

def train_model(data):
    # Dummy training function using a simple linear regression model
    features = data[['feature1', 'feature2']]  # Adjust features based on your dataset
    target = data['target']  # Adjust target based on your dataset

    model = LinearRegression()
    model.fit(features, target)

    # Save the trained model
    joblib.dump(model, 'trained_model.joblib')

# Dummy data for training (replace this with your actual dataset)
data_for_training = pd.DataFrame({
    'feature1': [1, 2, 3],
    'feature2': [4, 5, 6],
    'target': [10, 15, 20]
})

train_model(data_for_training)
