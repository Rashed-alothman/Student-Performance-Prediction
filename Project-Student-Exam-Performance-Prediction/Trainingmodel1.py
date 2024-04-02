import logging
import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from joblib import dump
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
import shap

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(filename):
    '''Load dataset from a CSV file.'''
    try:
        df = pd.read_csv(filename)
        logging.info('Dataset loaded successfully')
        return df
    except Exception as e:
        logging.error(f"Error occurred while loading data: {e}")
        raise

def preprocess_data(df):
    '''Extract features and target variable, and split data into training and testing sets.'''
    try:
        x = df[['Study Hours', 'Previous Exam Score']]
        y = df['Pass/Fail']
        logging.info('Features and target variable extracted')
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        logging.info('Data split into training and testing sets')
        return x_train, x_test, y_train, y_test
    except Exception as e:
        logging.error(f"Error occurred while preprocessing data: {e}")
        raise

def train_model(x_train, y_train):
    '''Train a logistic regression model on the training data.'''
    try:
        # Define the pipeline
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('normalizer', Normalizer()),
            ('logreg', LogisticRegression(solver='liblinear'))
        ])
        # Convert x_train to a DataFrame if it's not already
        if not isinstance(x_train, pd.DataFrame):
            x_train = pd.DataFrame(x_train, columns=['Study Hours', 'Previous Exam Score'])
        # Use the pipeline to fit
        scores = cross_val_score(pipe, x_train, y_train, cv=5)
        logging.info(f'Cross-validation scores: {scores}')
        pipe.fit(x_train, y_train)
        return pipe
    except Exception as e:
        logging.error(f"Error occurred while training model: {e}")
        raise

def handle_imbalance(x, y):
    smote = SMOTE()
    x_res, y_res = smote.fit_resample(x, y)
    return x_res, y_res

def save_model(model, filename):
    '''Save the trained model to a file.'''
    try:
        dump(model, filename)
        logging.info(f'Model saved to {filename}')
    except Exception as e:
        logging.error(f"Error occurred while saving model: {e}")
        raise

def evaluate_model(model, x_test, y_test):
    '''Evaluate the model on the test data and print the classification report.'''
    try:
        test_predictions = model.predict(x_test)
        accuracy = accuracy_score(y_test, test_predictions)
        logging.info(f'Model Accuracy on Test Set: {accuracy:.2f}')
        print(classification_report(y_test, test_predictions))
    except Exception as e:
        logging.error(f"Error occurred while evaluating model: {e}")
        raise

def explain_model(pipeline, x_train):
    '''Explain the model using SHAP values.'''
    try:
        # Compute SHAP values
        logging.info('Computing SHAP values...')
        explainer = shap.Explainer(pipeline.named_steps['logreg'].predict_proba, x_train)
        explanation = explainer(x_train)

        # Extract SHAP values from the Explanation object
        shap_values = explanation.values

        # Plot SHAP values
        logging.info('Plotting SHAP values...')
        shap.summary_plot(shap_values, x_train, plot_type="bar")


        # Plot SHAP summary
        plt.title('SHAP Summary')
        shap.summary_plot(shap_values, x_train)


        
        logging.info('Model explanation complete.')
    except Exception as e:
        logging.error(f"Error occurred while explaining model: {e}")
        raise

def plot_predictions(y_test, y_pred):
    '''Plot the predicted values against the actual values.'''
    try:
        logging.info('Plotting predictions...')
        plt.figure(figsize=(8, 8))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.xlabel('Actual values')
        plt.ylabel('Predicted values')
        plt.title('Actual vs Predicted values')

        # Add a line for perfect predictions
        min_val = min(min(y_test), min(y_pred))
        max_val = max(max(y_test), max(y_pred))
        if min_val == max_val:
            min_val -= 0.1  # Subtract a small amount from the lower limit
            max_val += 0.1  # Add a small amount to the upper limit
        plt.plot([min_val, max_val], [min_val, max_val], color='red')
        plt.show()
        logging.info('Plotting complete.')
    except Exception as e:
        logging.error(f"Error occurred while plotting predictions: {e}")
        raise
    
def main():
    '''Main function to orchestrate the data loading, preprocessing, model training, model saving, and model evaluation.'''
    try:
        logging.debug('Loading data...')
        df = load_data('student_exam_data.csv')
        
        logging.debug('Preprocessing data...')
        x_train, x_test, y_train, y_test = preprocess_data(df)
 
        logging.debug('Handling imbalance...')
        x_train, y_train = handle_imbalance(x_train, y_train)


        logging.debug('Training model...')
        pipe = train_model(x_train, y_train)
        
        logging.debug('Saving model...')
        save_model(pipe, 'model.joblib')
        
        logging.debug('Predicting test data...')
        y_pred = pipe.predict(x_test)
        
        logging.debug('Evaluating model...')
        evaluate_model(pipe, x_test, y_test) 
        
        logging.debug('Explaining model...')
        explain_model(pipe, x_train)
        
        logging.debug('Plotting predictions...')
        plot_predictions(y_test, y_pred)
        
        logging.info('All tasks completed successfully.')
    except FileNotFoundError:
        logging.error('The specified file was not found.')
    except KeyError:
        logging.error('One of the specified columns was not found in the dataset.')
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    main()