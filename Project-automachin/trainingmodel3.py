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
# pip install tpot pandas scikit-learn matplotlib seaborn shap

# Initialize logging for informative output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the dataset with robust error handling
try:
    df = pd.read_csv('testing_data_final.csv')  # Ensure correct path to your dataset
    logging.info("Dataset successfully loaded.")
except FileNotFoundError:
    logging.error("The dataset file was not found.")
    raise
except Exception as e:
    logging.error(f"An unexpected error occurred while loading the dataset: {e}")
    raise

# Define features and target variable
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

# Normalize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model using TPOT
tpot = TPOTRegressor(generations=5, population_size=50, verbosity=2, random_state=42)
tpot.fit(X_train_scaled, y_train)

# Evaluate the model's performance
logging.info(f"TPOT R^2 score on test data: {tpot.score(X_test_scaled, y_test)}")

# Export the best model found by TPOT
tpot.export('tpot_best_model.py')

# Save the model to a pickle file
with open('tpot_automl_model.pkl', 'wb') as f:
    pickle.dump(tpot.fitted_pipeline_, f)

# Serialize the scaler object for future use
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
logging.info("Scaler object has been saved.")

# Proceed with SHAP analysis
try:
    # Review TPOT pipeline steps to ensure no additional transformation is adding features
    print(tpot.fitted_pipeline_)
    
    # Exclude the final estimator and create a transformation pipeline
    transformation_pipeline = Pipeline(tpot.fitted_pipeline_.steps[:-1])

    # Transform X_test using the transformation pipeline
    transformed_X_test = transformation_pipeline.transform(X_test)

    # Confirm the shape of transformed_X_test
    logging.info(f"Transformed test data shape after excluding the final estimator: {transformed_X_test.shape}")

    # Initialize SHAP explainer with the model's predict function and transformed test data
    model_predict_function = tpot.fitted_pipeline_.steps[-1][-1].predict
    explainer = shap.Explainer(model_predict_function, transformed_X_test)

    # Generate SHAP values
    shap_values = explainer(transformed_X_test)

    # Check the shape of the SHAP values to confirm they match the expected feature count
    logging.info(f"SHAP values shape: {shap_values.shape}")

    # Visualize SHAP values
    plt.figure()
    shap.summary_plot(shap_values.values[:, :9], transformed_X_test[:, :9], feature_names=features)
    plt.savefig('shap_summary_plot.png')
    logging.info("SHAP summary plot generated successfully.")
except Exception as e:
    logging.error(f"Error during SHAP analysis: {e}")