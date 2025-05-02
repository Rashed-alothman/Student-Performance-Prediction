import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import shap
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Assuming auto-sklearn is installed
    from autosklearn.regression import AutoSklearnRegressor
except ImportError as e:
    logging.error("Auto-sklearn is not installed. Please install it to proceed.")
    raise e

# Load the dataset
try:
    df = pd.read_csv('/mnt/data/testing_data_final.csv')
except FileNotFoundError as e:
    logging.error("The dataset file was not found.")
    raise e
except Exception as e:
    logging.error(f"An error occurred while loading the dataset: {e}")
    raise e

# Define features and target
features = [
    'sem_present_count', 'sem_absent_count', 'sem_eval_lec_test_1_mark',
    'sem_eval_lab_test_1_mark', 'semester_evaluation_mid_mark',
    'sem_eval_lec_test_2_mark', 'sem_eval_lab_test_2_mark',
    'semester_evaluation_pre_gtu_mark', 'semester_evaluation_internal_mark'
]
target = 'semester_evaluation_gtu_mark'

# Splitting and scaling the dataset
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# AutoML model training
try:
    automl = AutoSklearnRegressor(time_left_for_this_task=3600, per_run_time_limit=300, n_jobs=-1)
    automl.fit(X_train_scaled, y_train)
except Exception as e:
    logging.error(f"An error occurred during AutoML model training: {e}")
    raise e

# Model evaluation
try:
    y_pred = automl.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    logging.info(f"MAE: {mae:.2f}, MSE: {mse:.2f}, RMSE: {rmse:.2f}")
except Exception as e:
    logging.error(f"An error occurred during model evaluation: {e}")

# SHAP explainer creation and saving
try:
    explainer = shap.KernelExplainer(automl.predict, shap.kmeans(X_train_scaled, 50))
    with open('shap_explainer.pkl', 'wb') as explainer_file:
        pickle.dump(explainer, explainer_file)
except Exception as e:
    logging.error(f"Failed to create or save SHAP explainer: {e}")

# Save the model and scaler
try:
    with open('automl_model.pkl', 'wb') as model_file:
        pickle.dump(automl, model_file)
    with open('scaler.pkl', 'wb') as scaler_file:
        pickle.dump(scaler, scaler_file)
except Exception as e:
    logging.error(f"An error occurred while saving the model or scaler: {e}")

# Optionally, log the best pipeline found
try:
    logging.info(f"Best ML pipeline: {automl.show_models()}")
except Exception as e:
    logging.error(f"Failed to retrieve or log the best ML pipeline: {e}")