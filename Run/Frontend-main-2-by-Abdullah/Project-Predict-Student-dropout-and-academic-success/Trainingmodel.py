import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, OneHotEncoder,Normalizer
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from joblib import dump
import seaborn as sns
import sys
from scipy.stats import randint 
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

def preprocess_data(df):
    '''Preprocesses the data and splits it into training and testing sets.'''
    try:
        # Drop rows with missing target values
        df = df.dropna(subset=['Target'])

        # Split the dataset into features and target variable
        X = df.drop('Target', axis=1)
        y = df['Target']
        
        # Encode the target variable
        y = y.map({'Dropout': 0, 'Graduate': 1})
        
        # Split the data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        logging.info("Data split into training and testing sets.")
        # Remove rows with NaN in the target variable
        y_train = y_train.dropna()
        x_train = x_train.loc[y_train.index]
        
        # Remove rows with NaN in the target variable from testing set
        y_test = y_test.dropna()
        x_test = x_test.loc[y_test.index]

        return x_train, x_test, y_train, y_test
    except Exception as e:
        logging.error(f"An error occurred while preprocessing the data: {e}")
        raise


def build_pipeline(x_train):
    try:
        # Define preprocessing for numeric columns (scale them)
        numeric_features = x_train.select_dtypes(include=['int64', 'float64']).columns
        numeric_transformer = Pipeline(steps=[
            ('normalizer', Normalizer()),  # Normalization step
            ('scaler', StandardScaler())    # Standardization step
        ])

        # Define preprocessing for categorical columns (encode them)
        categorical_features = x_train.select_dtypes(include=['object', 'bool']).columns
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Create preprocessing steps by combining numeric and categorical transformations
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        # Create the pipeline with the RandomForest classifier
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        # Define the parameter distribution for RandomizedSearchCV
        param_dist = {
            'classifier__n_estimators': randint(100, 500),
            'classifier__max_depth': [None] + list(randint(1, 50).rvs(size=10)),
            'classifier__min_samples_split': randint(2, 20),
            'classifier__min_samples_leaf': randint(1, 20),
            'classifier__bootstrap': [True, False],
            'classifier__criterion': ['gini', 'entropy']
        }

        # Use RandomizedSearchCV to find the best parameters
        random_search = RandomizedSearchCV(pipeline, param_distributions=param_dist, n_iter=100, cv=5, scoring='accuracy', random_state=42)

        logging.info("Pipeline and RandomizedSearchCV created successfully.")
        return random_search
    except Exception as e:
        logging.error(f"An error occurred while building the pipeline: {e}")
        raise

def train_and_evaluate_model(random_search, x_train, y_train, x_test, y_test):
    '''Trains the model and evaluates its performance.'''
    try:
        # Fit the pipeline to the training data
        random_search.fit(x_train, y_train)
        
        # Print the best parameters
        logging.info(f"Best parameters: {random_search.best_params_}")
        
        # Predict on the test data
        y_pred = random_search.predict(x_test)
        
        # Evaluate the model
        # Calculate the accuracy
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f"Model Accuracy: {accuracy}")
        # Generate the classification report
        report = classification_report(y_test, y_pred)
        logging.info(f"Classification Report:\n{report}")
        # Perform cross-validation
        cv_scores = cross_val_score(random_search.best_estimator_, x_train, y_train, cv=5)
        logging.info(f"Cross-validation scores: {cv_scores}")
        logging.info(f"Average cross-validation score: {cv_scores.mean():.2f}")


    except Exception as e:
        logging.error(f"An error occurred during model training and evaluation: {e}")
        raise


def visualize_performance(random_search, x_test, y_test):
    '''Visualizes the performance of the model.'''
    try:
        # Predict the test set results
        y_pred = random_search.predict(x_test)

        # Generate the confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        # Plot using seaborn
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt="d", cmap='Blues', xticklabels=['Predicted Negative', 'Predicted Positive'], yticklabels=['Actual Negative', 'Actual Positive'])
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.title('Confusion Matrix')
        plt.show()
        
        # Plot feature importances
        feature_names = x_test.columns
        importances = random_search.named_steps['classifier'].feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10, 8))
        plt.title('Feature Importances')
        plt.bar(range(x_test.shape[1]), importances[indices], color='b', align='center')
        plt.xticks(range(x_test.shape[1]), feature_names[indices], rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
        # Plot ROC Curve
        y_score = random_search.predict_proba(x_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_score)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC)')
        plt.legend(loc="lower right")
        plt.show()
    except Exception as e:
        logging.error(f"An error occurred during the visualization: {e}")
        raise

def save_model(pipeline, filename='model.joblib'):
    """Saves the trained pipeline to a file."""
    try:
        dump(pipeline, filename)
        logging.info(f"Model saved to {filename}.")
    except Exception as e:
        logging.error(f"Failed to save the model: {e}")


def main():
    try:
        logging.info("Starting the script...")
        
        # Load your dataset
        logging.info("Loading the dataset...")
        df = load_data("dataset.csv")  # Update this path to your new dataset's location
        logging.info("Dataset loaded successfully.")

        # Preprocess the data
        logging.info("Preprocessing the data...")
        x_train, x_test, y_train, y_test = preprocess_data(df)
        logging.info("Data preprocessed successfully.")

        # Build the pipeline
        logging.info("Building the pipeline...")
        random_search = build_pipeline(x_train)
        logging.info("Pipeline built successfully.")

        # Train and evaluate the model
        logging.info("Training and evaluating the model...")
        train_and_evaluate_model(random_search, x_train, y_train, x_test, y_test)
        logging.info("Model trained and evaluated successfully.")

        # Visualize the model's performance
        logging.info("Visualizing the model's performance...")
        visualize_performance(random_search.best_estimator_, x_test, y_test)
        logging.info("Model performance visualized successfully.")

        # Save the model
        logging.info("Saving the model...")
        save_model(random_search.best_estimator_, 'my_trained_model.joblib')
        logging.info("Model saved successfully.")

        logging.info("Script completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during the execution of the script: {e}")
        raise

if __name__ == "__main__":
    main()
