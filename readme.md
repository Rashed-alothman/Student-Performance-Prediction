# Student Performance Prediction System

![GitHub](https://img.shields.io/badge/GitHub-Showcase-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Version](https://img.shields.io/badge/Version-0.9.0--beta-blueviolet)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

<div align="center">
  <img src="https://img.shields.io/badge/Educational-Technology-blue?style=for-the-badge" alt="Educational Technology"/>
  <br/>
  <h3>Advanced Machine Learning for Student Success Prediction</h3>
</div>

## 📚 Project Overview

This comprehensive student performance prediction system is a multifaceted machine learning project designed to help educational institutions proactively identify at-risk students and improve academic outcomes. The system includes three specialized prediction models that address different aspects of student performance:

1. **Final Exam Mark Predictor**: Predicts a student's final examination marks based on attendance, coursework, and internal assessments
2. **Dropout & Academic Success Predictor**: Identifies students at risk of dropping out with high accuracy (97%)
3. **Exam Performance Pass/Fail Predictor**: Forecasts whether a student will pass or fail upcoming exams

> **Note**: This project began as a university assignment but has evolved into a personal ongoing project. It is currently under active development with regular improvements and bug fixes.

## 🧠 Machine Learning Models

### 1. Student Final Exam Mark Predictor

- **Type**: Random Forest Regressor
- **Features**:
  - Attendance records (present/absent counts)
  - Lecture test marks
  - Lab test marks
  - Mid-semester evaluation marks
  - Pre-GTU marks
  - Internal assessment marks
- **Performance**:
  - Low Mean Absolute Error (MAE)
  - Low Root Mean Squared Error (RMSE)
  - Feature importance visualization
  - SHAP explainability for transparent predictions

### 2. Student Dropout & Academic Success Predictor

- **Type**: Random Forest Classifier with hyperparameter tuning via RandomizedSearchCV
- **Features**:
  - Demographic information
  - Previous academic performance
  - Engagement metrics
  - Socioeconomic indicators
- **Performance**:
  - Accuracy: 97%
  - Comprehensive classification report
  - Confusion matrix visualization
  - ROC curve analysis
  - Cross-validation for robust evaluation

### 3. Student Exam Performance Pass/Fail Predictor

- **Type**: Logistic Regression with Pipeline (StandardScaler + Normalizer)
- **Features**:
  - Study hours
  - Previous exam scores
- **Performance**:
  - Accuracy: 88%
  - SMOTE handling for class imbalance
  - Cross-validation scoring
  - Intuitive prediction visualization

## 🌟 Key Features

- **Interactive Web Interface**: Multi-page web application with step-by-step forms
- **Multi-step Prediction Forms**: User-friendly data collection
- **Dark Mode Support**: Toggle between light and dark themes
- **Explainable AI**: SHAP values help interpret prediction factors
- **Data Visualization**: Comprehensive visual representations of model performance
- **Batch Processing**: Upload CSV files to process multiple students at once
- **Error Handling**: Robust error management throughout
- **Responsive Design**: Works well across different device sizes

## 🛠️ Technical Implementation

### Backend

- **Framework**: Flask web server
- **Machine Learning**: scikit-learn, SHAP for explainability
- **Data Processing**: pandas, numpy for data manipulation
- **Model Persistence**: Serialized models via joblib/pickle
- **Validation**: Cross-validation and testing methodology

### Frontend

- **Structure**: HTML5 for content structure
- **Styling**: CSS3 with responsive design
- **Interaction**: JavaScript for dynamic behavior
- **Animation**: CSS transitions and animations
- **User Experience**: Multi-step forms with validation

## 📊 Model Results

### Final Exam Mark Predictor

- Mean Absolute Error: < 5 marks
- Feature importance shows attendance and mid-term scores as key predictors

### Dropout Risk Predictor

- High precision in identifying at-risk students
- Low false positive rate to prevent unnecessary interventions
- Feature importance highlights key early warning signs

### Pass/Fail Predictor

- 88% accuracy in predicting exam outcomes
- Balanced precision and recall metrics

## 🔍 Use Cases

1. **Early Intervention**: Identify at-risk students before academic failure
2. **Resource Allocation**: Focus additional support on students who need it most
3. **Student Self-Assessment**: Allow students to understand factors affecting their performance
4. **Academic Planning**: Help advisors make data-driven recommendations
5. **Institutional Planning**: Improve overall retention and success rates

## 📱 Screenshots

_(Screenshots coming soon - UI/UX improvements in progress)_

## ⚠️ Current Status and Known Issues

This project is currently in active development. While the core functionality works, there are some known issues:

- Some UI elements need refinement for better mobile responsiveness
- Occasional prediction inconsistencies with certain edge case inputs
- CSV batch upload functionality has validation limitations
- Model retraining pipeline needs improvement for new data incorporation
- Some browser compatibility issues in Internet Explorer and older browsers

I am actively working on resolving these issues and implementing new features. Bug reports, feature requests, and contributions are welcome!

## 🚀 Roadmap and Future Enhancements

- [ ] User authentication and student profiles
- [ ] Mobile application version
- [ ] Additional predictive models for other academic metrics
- [ ] Integration with institutional LMS platforms
- [ ] Long-term tracking and performance analytics
- [ ] Recommendation engine for improvement strategies
- [ ] Enhanced data visualization dashboard
- [ ] API endpoints for third-party integration
- [ ] Multi-language support
- [ ] Automated model retraining with new data
- [ ] Unit and integration test coverage

## 🔧 Project Structure

```
project_student_performance/
├── Project-Predict-Student-dropout-and-academic-success/  # Dropout prediction model
│   ├── app.py                 # Flask application
│   ├── Trainingmodel.py       # Model training script
│   ├── static/                # Frontend assets
│   └── templates/             # HTML templates
├── Project-Student-Exam-Performance-Prediction/      # Pass/fail prediction
│   ├── app4.py                # Flask application
│   ├── Trainingmodel1.py      # Model training script
│   ├── static/                # Frontend assets
│   └── templates/             # HTML templates
├── project-Student-Performace/                  # Final exam mark predictor
│   ├── app.py                 # Flask application
│   ├── Trainigmodel4.py       # Model training script
│   ├── static/                # Frontend assets
│   └── templates/             # HTML templates
└── Project-Run/               # Integrated web application
    ├── Frontend-main-Rashed/  # Combined frontend
    │   ├── Main/              # Main application
    │   │   ├── Run.py         # Main application entry point
    │   │   ├── Static/        # Static assets
    │   │   └── templates/     # HTML templates
    │   └── project folders    # Individual project components
    └── ...
```

## 🧪 Technologies Used

- **Python**: Core programming language
- **Flask**: Web framework
- **scikit-learn**: Machine learning library
- **pandas/numpy**: Data manipulation libraries
- **SHAP**: Model explainability
- **Matplotlib/Seaborn**: Data visualization
- **joblib/pickle**: Model serialization
- **HTML/CSS/JavaScript**: Frontend development

## 🤝 Contributing

Contributions to this project are welcome and appreciated! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

I'm more than happy to review and merge valuable contributions. Whether it's bug fixes, feature enhancements, or documentation improvements - all help is welcome!

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Contact

If you have any questions, suggestions, or would like to collaborate, please feel free to reach out.

---

_This project originated as a university assignment and has evolved into a personal ongoing project. I apologize for any bugs or issues you may encounter - the system is continuously being improved. Thank you for your interest and understanding!_
