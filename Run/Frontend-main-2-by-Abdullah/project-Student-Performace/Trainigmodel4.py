import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score,RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler,Normalizer
from sklearn.pipeline import Pipeline
import shap
from joblib import dump # use joblib instead of pickle for efficiency
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    '''Loads data from a CSV file.'''
    try:
        df = pd.read_csv(file_path)
        logging.info("Dataset loaded successfully.")
        return df
    except FileNotFoundError:
        logging.error("Dataset file not found. Please check the file path.")
        raise
    except Exception as e:
        logging.error(f"An error occurred while loading the dataset: {e}")
        raise

def preprocess_data(df, features, target):
    '''Splits the data into training and testing sets.'''
    try:
        x_train, x_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)
        logging.info("Data split into training and testing sets.")

        return x_train, x_test, y_train, y_test
    except Exception as e:
        logging.error(f"An error occurred while preprocessing the data: {e}")
        raise

def train_model(x_train, y_train):
    '''Trains the model using a pipeline.'''
    try:

        logging.info("Setting up the pipeline...")
        # Set up the pipeline with the best parameters
        pipeline = Pipeline(steps=[
            ('normalizer', Normalizer()),
            ('scaler', StandardScaler()),
            ('model', RandomForestRegressor(
                n_estimators=400,
                min_samples_split=10,
                min_samples_leaf=1,
                max_features='sqrt',
                max_depth=100,
                bootstrap=True,
                random_state=42
            ))
        ])



        logging.info("Fitting the model...")

        # Fit the model
        pipeline.fit(x_train, y_train)

        # Get the 'scaler' and 'normalizer' steps
        #scaler = pipeline.named_steps['scaler']
        #normalizer = pipeline.named_steps['normalizer']
        # Create the explainer
        explainer = shap.Explainer(pipeline.predict, x_train)
        
        logging.info("Model trained successfully.")

        return pipeline, explainer #scaler, normalizer
    except Exception as e:
        logging.error(f"An error occurred while training the model: {e}")
        raise

def evaluate_model(pipeline, x_test, y_test):
    '''Evaluates the model and performs cross-validation.'''
    try:
        # Evaluate the model
        predictions = pipeline.predict(x_test)
        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        
        # Access the OOB Score
        if hasattr(pipeline.named_steps['model'], 'oob_score_'):
            oob_score = pipeline.named_steps['model'].oob_score_
            logging.info(f"Out-of-Bag Score: {oob_score}")
        
        logging.info(f"Model evaluation - MAE: {mae}, MSE: {mse}, RMSE: {rmse}")

        # Cross-validation
        scores = cross_val_score(pipeline, x_test, y_test, cv=5)
        logging.info(f"Cross-validation scores: {scores}")
        
    except Exception as e:
        logging.error(f"An error occurred while evaluating the model: {e}")
        raise

def explain_model(pipeline, x_train, x_test, y_test):
    '''Explains the model using SHAP values and plots the results.'''
    try:
        # Create a SHAP explainer and calculate SHAP values
        explainer = shap.TreeExplainer(pipeline.named_steps['model'])
        shap_values = explainer.shap_values(pipeline.named_steps['scaler'].transform(x_train))


        # Plot the SHAP values
        shap.summary_plot(shap_values, x_train, feature_names=x_train.columns)
        
        
        # Visualize the results obtained by using the RandomForest Regression model
        # Get the predicted values
        y_pred = pipeline.predict(x_test)

        # Plot the predicted values against the actual values
        plt.scatter(y_pred, y_test, color='blue')

        # Add a line representing perfect predictions
        min_val = min(min(y_pred), min(y_test))  # Find the minimum value among the predicted and actual values
        max_val = max(max(y_pred), max(y_test))  # Find the maximum value among the predicted and actual values
        plt.plot([min_val, max_val], [min_val, max_val], color='red')

        plt.xlabel('Predicted Values')
        plt.ylabel('Actual Values')
        plt.title('Predicted vs Actual Values')
        plt.show()

        # Plot decision tree
        tree_to_plot = pipeline.named_steps['model'].estimators_[0]
        plt.figure(figsize=(20, 10))
        plot_tree(tree_to_plot, feature_names=x_train.columns.tolist(), filled=True, rounded=True, fontsize=10)
        plt.title("Decision Tree from Random Forest")
        plt.show()
        

        return explainer
    except Exception as e:
        logging.error(f"An error occurred while explaining the model: {e}")
        raise

def save_model(pipeline, explainer, filepath):
    """
    Save the pipeline and explainer to a file.

    pipeline: trained pipeline to be saved
    explainer: fitted explainer to be saved
    filepath: destination file path
    """

    # Save the pipeline and SHAP explainer to disk
    try:
        dump({
            'pipeline': pipeline,
            'explainer': explainer
        }, filepath)
        logging.info(f'Pipeline and explainer saved at {filepath}')
    except Exception as e:
        logging.error(f"An error occurred while saving the pipeline and explainer: {e}")
        raise



# All your function definitions go here...

def main():
    logging.info("Starting the script...")

    # Define the features and the target variable based on your dataset

    features = [
        'sem_present_count', 'sem_absent_count', 'sem_eval_lec_test_1_mark',
        'sem_eval_lab_test_1_mark', 'semester_evaluation_mid_mark',
        'sem_eval_lec_test_2_mark', 'sem_eval_lab_test_2_mark',
        'semester_evaluation_pre_gtu_mark', 'semester_evaluation_internal_mark'
    ]
    target = 'semester_evaluation_gtu_mark'

    # Load your dataset
    logging.info("Loading data...")
    df = load_data('training_data_final.csv')  # Make sure to replace with your dataset's path

    # Preprocess the data
    logging.info("Preprocessing data...")
    x_train, x_test, y_train, y_test = preprocess_data(df, features, target)

    # Train the model
    logging.info("Training model...")
    pipeline,explainer = train_model(x_train, y_train)


    # Explain the model
    logging.info("Explaining model...")
    explainer = explain_model(pipeline, x_train, x_test, y_test) 

    # Save the model
    logging.info("Saving model...")
    save_model(pipeline , explainer, 'my_model.joblib')

    # Evaluate the model
    logging.info("Evaluating model...")
    evaluate_model(pipeline, x_test, y_test)

    logging.info("Script completed successfully.")

if __name__ == "__main__":
    main()