import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np

# Load the dataset
df = pd.read_csv('testing_data_final.csv')

# Drop the id column as it is not a feature for the model
X = df.drop(columns=['id_semester_evaluation', 'semester_evaluation_gtu_mark'])

# The target variable is the final exam mark
y = df['semester_evaluation_gtu_mark']

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize a StandardScaler
scaler = StandardScaler()

# Fit the scaler on the training data and transform both training and test sets
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize the Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the regressor
rf_regressor.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred = rf_regressor.predict(X_test_scaled)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

# Save the model to a file
with open('rf_model.pkl', 'wb') as model_file:
    pickle.dump(rf_regressor, model_file)

# Save the scaler for later use during predictions
with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)
