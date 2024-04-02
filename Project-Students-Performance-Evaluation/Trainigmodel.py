import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from joblib import dump
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    '''Loads data from a CSV file.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pandas.DataFrame: The loaded dataset.
        
    Raises:
        FileNotFoundError: If the dataset file is not found.
        Exception: If an error occurs while loading the dataset.
    '''
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

def train_model(x_train, y_train):
    '''Trains the model using a pipeline with normalization, scaling, and RandomizedSearchCV.
    
    Args:
        x_train (pandas.DataFrame): The training features.
        y_train (pandas.Series): The training target variable.
        
    Returns:
        sklearn.pipeline.Pipeline: The trained model.
        
    Raises:
        Exception: If an error occurs while training the model.
    '''
    try:
        # Define a pipeline
        pipeline = Pipeline(steps=[
            ('normalizer', Normalizer()),
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        # Define the parameter grid for RandomizedSearchCV
        param_distributions = {
            'classifier__n_estimators': [100, 200, 300, 400, 500],
            'classifier__max_depth': [None, 10, 20, 30, 40, 50],
            'classifier__min_samples_split': [2, 5, 10],
            'classifier__min_samples_leaf': [1, 2, 4],
            'classifier__bootstrap': [True, False]
        }

        # Initialize RandomizedSearchCV
        randomized_search = RandomizedSearchCV(pipeline, param_distributions, n_iter=100, cv=5, random_state=42, n_jobs=-1)

        # Fit the model
        randomized_search.fit(x_train, y_train)

        # Get the best estimator
        best_pipeline = randomized_search.best_estimator_

        logging.info(f"Best parameters found: {randomized_search.best_params_}")

        return best_pipeline
    except Exception as e:
        logging.error(f"An error occurred while training the model: {e}")
        raise

def evaluate_model(pipeline, x_test, y_test):
    '''Evaluates the model on the test set and plots predictions against actual values.
    
    Args:
        pipeline (sklearn.pipeline.Pipeline): The trained model.
        x_test (pandas.DataFrame): The test features.
        y_test (pandas.Series): The test target variable.
        
    Raises:
        Exception: If an error occurs while evaluating the model.
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
        raise

def visualize_results(model, X):
    '''Generates and displays important features from the model.
    
    Args:
        model (sklearn.pipeline.Pipeline): The trained model.
        X (pandas.DataFrame): The input features.
        
    Raises:
        Exception: If an error occurs while visualizing the results.
    '''
    try:
        feature_importances = model.named_steps['classifier'].feature_importances_
        indices = np.argsort(feature_importances)[::-1]
        plt.figure(figsize=(12, 6))
        plt.title("Feature Importances")
        plt.bar(range(X.shape[1]), feature_importances[indices],
                color="r", align="center")
        plt.xticks(range(X.shape[1]), indices)
        plt.xlim([-1, X.shape[1]])
        plt.xlabel('Feature Index')
        plt.ylabel('Importance')
        plt.show()
    except Exception as e:
        logging.error(f"An error occurred while visualizing the results: {e}")
        raise

def main():
    # Load your dataset
    df = load_data('DATA.csv')  

    # Define the features and the target variable
    features = [
    '1', # Categorized into 1 (18-21), 2 (22-25), 3 (above 26)
    '2', # Categorized into 1 (female), 2 (male)
    '3', # Categorized into 1 (private), 2 (state), 3 (other)
    '4', # Categorized from 1 (None) to 5 (Full)
    '5', # Categorized into 1 (Yes), 2 (No)
    '6', # Categorized into 1 (Yes), 2 (No)
    '7', # Categorized into 1 (Yes), 2 (No)
    '8', # Categorized from 1 (USD 135-200) to 5 (above 410)
    '9', # Categorized from 1 (Bus) to 4 (Other)
    '10', # Categorized from 1 (rental) to 4 (Other)
    '11', # Categorized from 1 (primary school) to 6 (Ph.D.)
    '12', # Same as mother's education
    '13', # Categorized from 1 (1) to 5 (5 or above)
    '14', # Categorized into 1 (married), 2 (divorced), 3 (died)
    '15', # Categorized from 1 (retired) to 6 (other)
    '16', # Categorized from 1 (retired) to 5 (other)
    '17', # Categorized from 1 (None) to 5 (more than 20 hours)
    '18', # Categorized from 1 (None) to 3 (Often) for non-scientific books/journals
    '19', # Categorized from 1 (None) to 3 (Often) for scientific books/journals
    '20', # Categorized into 1 (Yes), 2 (No) for attendance to seminars/conferences
    '21', # Categorized into 1 (positive), 2 (negative), 3 (neutral) for the impact of projects/activities
    '22', # Categorized from 1 (always) to 3 (never) for class attendance
    '23', # Categorized from 1 (alone) to 3 (not applicable) for preparation to midterm exams 1
    '24', # Categorized from 1 (closest date to the exam) to 3 (never) for preparation to midterm exams 2
    '25', # Categorized from 1 (never) to 3 (always) for taking notes in classes
    '26', # Categorized from 1 (never) to 3 (always) for listening in classes
    '27', # Categorized from 1 (never) to 3 (always) for whether discussion improves interest/success
    '28', # Categorized from 1 (not useful) to 3 (not applicable) for the utility of flip-classroom
    '29', # Categorized from 1 (<2.00) to 5 (above 3.49) for cumulative GPA last semester
    '30' # Categorized from 1 (<2.00) to 5 (above 3.49) for expected cumulative GPA in graduation
]

    target = 'GRADE' # The student's output grade, categorized from 0 (Fail) to 7 (AA), representing their performance

    # The features are chosen based on the provided attribute information.
    # Each feature corresponds to a specific aspect of the student's background, academic habits, or environmental factors.
    # The target, 'output_grade', is the outcome variable we aim to predict based on the features.
    df[features]
    df[target]

    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

    # Train the model
    best_pipeline = train_model(x_train, y_train)

    # Evaluate the model and plot predictions
    evaluate_model(best_pipeline, x_test, y_test)
    
    # Visualize the results
    visualize_results(best_pipeline, x_train)

    # Save the best model to a file
    dump(best_pipeline, 'best_random_forest_pipeline.joblib')

    logging.info("The best model was saved to 'best_random_forest_pipeline.joblib'.")

if __name__ == "__main__":
    main()

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
