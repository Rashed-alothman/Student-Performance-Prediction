import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tpot import TPOTRegressor
import pickle
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import shap
# Ensure you've installed all necessary libraries:
# pip install tpot pandas numpy scikit-learn matplotlib seaborn shap

# Initialize logging to provide information throughout the process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the dataset with error handling for potential issues
try:
    df = pd.read_csv('testing_data_final.csv')  # Update this path to where your dataset is located
except FileNotFoundError as e:
    logging.error("The dataset file was not found.")
    raise e
except Exception as e:
    logging.error(f"An unexpected error occurred while loading the dataset: {e}")
    raise e

# Define the features and target variable based on your dataset's columns
features = [
    'sem_present_count', 'sem_absent_count', 'sem_eval_lec_test_1_mark',
    'sem_eval_lab_test_1_mark', 'semester_evaluation_mid_mark',
    'sem_eval_lec_test_2_mark', 'sem_eval_lab_test_2_mark',
    'semester_evaluation_pre_gtu_mark', 'semester_evaluation_internal_mark'
]
target = 'semester_evaluation_gtu_mark'

# Split the dataset into training and test sets
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features to normalize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model using TPOT
tpot = TPOTRegressor(generations=5, population_size=50, verbosity=2, random_state=42)
tpot.fit(X_train_scaled, y_train)

# Evaluate the model
logging.info(f"TPOT R^2 score on test data: {tpot.score(X_test_scaled, y_test)}")

# Export the best model found by TPOT
tpot.export('tpot_best_model.py')

# Save the scaler using pickle for later use
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Assuming SHAP explanations are desired for the TPOT model
# Note: Directly using SHAP with TPOT might require extracting the final model or adapting based on the pipeline
try:
    # The TPOT model is a sklearn pipeline, so we extract the final estimator for SHAP
    model = tpot.fitted_pipeline_.steps[-1][-1]
    explainer = shap.Explainer(model.predict, X_train_scaled)
    shap_values = explainer(X_test_scaled)
    
    # Visualize the SHAP values for feature importance
    shap.summary_plot(shap_values, X_test_scaled, feature_names=features)

except Exception as e:
    logging.error(f"An error occurred while generating SHAP explanations: {e}")

# Note: The SHAP visualization will work best in a Jupyter notebook or similar environment
# For non-interactive environments, consider saving the plots as files
