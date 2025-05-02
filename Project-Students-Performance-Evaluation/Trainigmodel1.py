# Standard library imports
import argparse
import logging
import sys
import os
# Third party imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from joblib import dump, load


# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    '''Loads data from a CSV file.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pandas.DataFrame: The loaded dataset.
    '''
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Dataset loaded successfully from {file_path}.")
        return df
    except FileNotFoundError:
        logging.error(f"Dataset file {file_path} not found. Please check the file path.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred while loading the dataset from {file_path}: {e}")
        sys.exit(1)

def train_model(x_train, y_train):
    '''Trains the model using a pipeline with normalization, scaling, and RandomizedSearchCV.
    
    Args:
        x_train (pandas.DataFrame): The training features.
        y_train (pandas.Series): The training target variable.
        
    Returns:
        sklearn.pipeline.Pipeline: The trained model.
    '''
    try:
        # Define a pipeline
        pipeline = Pipeline(steps=[
            ('normalizer', Normalizer()),
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(
            n_estimators=800,
            min_samples_split=8,
            min_samples_leaf=7,
            max_features=0.5,
            max_depth=100,
            bootstrap=True,
            random_state=42))
        ])
        logging.info("Pipeline created successfully.")

        # Train the model
        pipeline.fit(x_train, y_train)
        logging.info("Model trained successfully.")

        return pipeline
    except Exception as e:
        logging.error(f"An error occurred while training the model: {e}")
        sys.exit(1)

def evaluate_model(pipeline, x_test, y_test):
    '''Evaluates the model on the test set and plots predictions against actual values.
    
    Args:
        pipeline (sklearn.pipeline.Pipeline): The trained model.
        x_test (pandas.DataFrame): The test features.
        y_test (pandas.Series): The test target variable.
    '''
    try:
        # Make predictions
        predictions = pipeline.predict(x_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, predictions)
        
        logging.info(f"Model evaluation - Accuracy: {accuracy}")

        # Plot the predicted values against the actual values
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, predictions, alpha=0.5)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title("Predicted vs. Actual Values")
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
        plt.show()
        
    except Exception as e:
        logging.error(f"An error occurred while evaluating the model: {e}")
        sys.exit(1)

def visualize_results(model, x):
    '''Generates and displays important features from the model.
    
    Args:
        model (sklearn.pipeline.Pipeline): The trained model.
        X (pandas.DataFrame): The training features.
    '''
    try:
        feature_importances = model.named_steps['classifier'].feature_importances_
        indices = np.argsort(feature_importances)[::-1]
        plt.figure(figsize=(12, 6))
        plt.title("Feature Importances")
        plt.bar(range(x.shape[1]), feature_importances[indices],
                color="r", align="center")
        plt.xticks(range(x.shape[1]), indices)
        plt.xlim([-1, x.shape[1]])
        plt.xlabel('Feature Index')
        plt.ylabel('Importance')
        plt.show()
    except Exception as e:
        logging.error(f"An error occurred while visualizing the results: {e}")
        sys.exit(1)

def main(args):
    '''Main function to execute the script.
    
    Args:
        args (argparse.Namespace): The command-line arguments.
        
    '''


    directory = 'C:\\Users\\rashe\\.vscode\\.vscode\\project\\student_performance_project\\ProjectNew'

    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
    elif not os.access(directory, os.W_OK):
        print(f"The directory {directory} is not writable.")
    else:
        print(f"The directory {directory} exists and is writable.")
    # Log the start of the script
    logging.info("Script started.")

    # Load your dataset
    logging.info("Loading dataset...")
    df = load_data(args.dataset_path)
    logging.info("Dataset loaded.")


    # Define the features and the target variable
    logging.info("Defining features and target variable...")
    features = args.features
    target = args.target

    # Split the data into training and testing sets
    logging.info("Splitting data into training and testing sets...")
    x_train, x_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)
    logging.info("Data split.")

    # Train the model
    logging.info("Training the model...")
    best_pipeline = train_model(x_train, y_train)
    logging.info("Model trained.")

    # Evaluate the model and plot predictions
    logging.info("Evaluating the model and plotting predictions...")
    evaluate_model(best_pipeline, x_test, y_test)
    logging.info("Model evaluation and plotting completed.")

    # Visualize the results
    logging.info("Visualizing the results...")
    visualize_results(best_pipeline, x_train)
    logging.info("Results visualization completed.")

    # Save the best model to a file
    logging.info("Saving the best model to a file...")
    model_output_path_with_filename = os.path.join(args.model_output_path, 'best_model.joblib')
    dump(best_pipeline, model_output_path_with_filename)
    logging.info(f"The best model was saved to {model_output_path_with_filename}.")

    logging.info("Script completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a model to predict student grades.')
    parser.add_argument('--dataset_path', type=str, required=True, help='Path to the dataset CSV file.')
    parser.add_argument('--model_output_path', type=str, required=True, help='Path to save the trained model.')
    parser.add_argument('--features', type=str, nargs='+', required=True, help='List of feature column names.')
    parser.add_argument('--target', type=str, required=True, help='Name of the target column.')
    args = parser.parse_args()
    
    main(args)

    logging.info(f"The best model was saved to {args.model_output_path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a model to predict student grades.')
    parser.add_argument('--dataset_path', type=str, required=True, help='Path to the dataset CSV file.')
    parser.add_argument('--model_output_path', type=str, required=True, help='Path to save the trained model.')
    parser.add_argument('--features', type=str, nargs='+', required=True, help='List of feature column names.')
    parser.add_argument('--target', type=str, required=True, help='Name of the target column.')
    args = parser.parse_args()

    main(args)

# Features explanation based on the dataset's attributes:

# 'student_age': Categorical variable indicating the age group of the student.
# Age groups are divided as follows: 1 for ages 18-21, 2 for ages 22-25, and 3 for ages above 26.

# 'sex': Categorical variable indicating the sex of the student. 1 for female and 2 for male.

# 'graduated_high_school_type': Type of high school the student graduated from.
# Categorized as 1 for private, 2 for state, and 3 for other types of high schools.

# 'scholarship_type': Indicates the type of scholarship received by the student.
# Ranges from 1 (None) to 5 (Full scholarship).

# 'additional_work': Whether the student is engaged in additional work outside of studies.
# 1 for Yes, indicating the student has additional work, and 2 for No, indicating they do not.

# 'artistic_sports_activity': Indicates if the student regularly participates in artistic or sports activities.
# 1 for Yes and 2 for No.

# 'have_partner': Indicates whether the student has a partner. 1 for Yes and 2 for No.

# 'total_salary': Categorical variable representing the total salary range of the student, if available.
# Divided into categories from 1 (USD 135-200) to 5 (above USD 410).

# 'transportation': The primary mode of transportation used by the student to get to the university.
# Categories include 1 for Bus, 2 for Private car/taxi, 3 for Bicycle, and 4 for Other.

# 'accommodation_type': Type of accommodation the student lives in while attending university in Cyprus.
# Categories are 1 for Rental, 2 for Dormitory, 3 for Living with family, and 4 for Other.

# 'mother_education' and 'father_education': Represent the highest level of education completed by the student's parents.
# Categories range from 1 (Primary school) to 6 (Ph.D.).

# 'siblings_count': The number of siblings the student has. Categories range from 1 (1 sibling) to 5 (5 or more siblings).

# 'parental_status': The marital status of the student's parents. 
# Categorized as 1 for Married, 2 for Divorced, and 3 for Deceased (one or both).

# 'mother_occupation' and 'father_occupation': The occupation of the student's parents.
# Categories for each parent range from 1 (Retired) to 6 (Other).

# 'weekly_study_hours': The number of hours per week the student spends studying outside of class.
# Categories range from 1 (None) to 5 (More than 20 hours).

# 'reading_freq_non_sci' and 'reading_freq_sci': Frequency of reading non-scientific and scientific books/journals, respectively.
# Each categorized from 1 (None) to 3 (Often).

# 'attendance_seminars', 'impact_of_activities', 'attendance_classes', 'prep_midterm_1', 'prep_midterm_2', 
# 'taking_notes', 'listening_classes', 'discussion_impact', 'flip_classroom':
# These features represent various academic habits and attitudes towards learning, 
# such as seminar attendance, the impact of extracurricular activities, class attendance, 
# exam preparation methods, note-taking, listening habits, the value of discussions, and the perceived utility of flip-classrooms.

# 'cumulative_gpa_last_sem' and 'expected_cumulative_gpa':
# These features indicate the student's GPA in the last semester and their expected GPA at graduation, respectively.
# Categories range from 1 (<2.00) to 5 (above 3.49).

# 'output_grade': The target variable, representing the grade the student received.
# Categorized from 0 (Fail) to 7 (AA), indicating the student's performance.