import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle

# Hypothetical dataset
data = {
    'Study Hours': [4, 5, 2, 6, 3, 7, 8, 5],
    'Previous Exam Score': [75, 82, 60, 88, 65, 92, 95, 80],
    'Pass/Fail': [1, 1, 0, 1, 0, 1, 1, 1]  # 1 for Pass, 0 for Fail
}

df = pd.DataFrame(data)

# Feature Engineering
X = df[['Study Hours', 'Previous Exam Score']]
y = df['Pass/Fail']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a logistic regression model
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

# Save the model to a file
with open('model_pkl', 'wb') as model_file:
    pickle.dump(lr_model, model_file)

# Define a scaler for feature scaling
scaler = StandardScaler()

# Fit and transform the scaler on the entire dataset
X_scaled = scaler.fit_transform(X)

# Save the scaler for later use during predictions
with open('scaler_pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)

# Calculate accuracy on the test set
test_predictions = lr_model.predict(X_test)
accuracy = (y_test == test_predictions).mean()
print(f'Model Accuracy on Test Set: {accuracy:.2f}')

