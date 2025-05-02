// Improved and Organized JavaScript for Handling Form Steps and Predictions

let currentStep = 1; // Track the current form step

// Moves to a specified step
const changeStep = (newStep) => {
    const current = document.querySelector(`.step[data-step="${currentStep}"]`);
    const next = document.querySelector(`.step[data-step="${newStep}"]`);
    
    if (current) current.style.display = 'none';
    if (next) next.style.display = 'block';
    
    currentStep = newStep ;
}
//      Advances to the next form step
     function nextStep () {

     if (!validateAttendance()) return;
     if (!validateAdditionalFields()) return;

     changeStep(currentStep + 1);
     }
      //Goes back to the previous form step
     function prevStep() {
        changeStep(currentStep - 1);
     }

     const predict = async () => {
        const formData = collectFormData();
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
    
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            displayPredictionResult(data);
        } catch (error) {
            console.error('Prediction error:', error);
            displayError('Failed to get prediction');
        }
    };
// Function to display custom alert message
// Function to display custom alert message
function customAlert(message) {
    const alertContainer = document.getElementById('customAlertContainer');
    alertContainer.textContent = message;
    alertContainer.style.display = 'block';

    // Hide the alert after a few seconds (e.g., 5 seconds)
    setTimeout(() => {
        alertContainer.style.display = 'none';
    }, 5000); // Adjust the time as needed
}

// Function to validate attendance and absence counts
function validateAttendance() {
    const semPresentCount = parseFloat(document.getElementById('sem_present_count').value);
    const semAbsentCount = parseFloat(document.getElementById('sem_absent_count').value);

    // Validate absence count not exceeding present count
    if (semAbsentCount > semPresentCount) {
        customAlert('You cannot enter a number greater than attendance or absence.');
        return false;
    }

    // Validate that attendance + absence <= 100
    const totalClasses = semPresentCount + semAbsentCount;
    if (totalClasses > 100) {
        customAlert('You must make the total not exceed 100.');
        return false;
    }

    // Validate that absence does not exceed the complement of attendance to reach 100
    const maxAbsence = 100 - semPresentCount;
    if (semAbsentCount > maxAbsence) {
        customAlert('You cannot enter a number greater than 30.');
        return false;
    }

    return true;
}

// Function to validate additional fields not exceeding 30
function validateAdditionalFields() {
    const additionalFields = [
        'sem_eval_lec_test_1_mark',
        'sem_eval_lab_test_1_mark',
        'semester_evaluation_mid_mark',
        'sem_eval_lec_test_2_mark',
        'sem_eval_lab_test_2_mark',
        'semester_evaluation_pre_gtu_mark',
        'semester_evaluation_internal_mark',
    ];

    for (let field of additionalFields) {
        const value = parseFloat(document.getElementById(field).value);
        if (value > 30) {
            customAlert('You cannot enter a number greater than 30.');
            return false;
        }
    }

    return true;
}

// Function to validate additional fields not exceeding 30
function validateAdditionalFields() {
    const additionalFields = [
        'sem_eval_lec_test_1_mark',
        'sem_eval_lab_test_1_mark',
        'semester_evaluation_mid_mark',
        'sem_eval_lec_test_2_mark',
        'sem_eval_lab_test_2_mark',
        'semester_evaluation_pre_gtu_mark',
        'semester_evaluation_internal_mark',
    ];

    for (let field of additionalFields) {
        const value = parseFloat(document.getElementById(field).value);
        if (value > 30) {
            customAlert('You cannot enter a number greater than 30.');
            return false;
        }
    }

    return true;
}
// Collects input values from the form
const collectFormData = () => {
    return {
        // Collect and parse form data here
        sem_present_count: parseFloat(document.getElementById('sem_present_count').value),
        sem_absent_count: parseFloat(document.getElementById('sem_absent_count').value),
        sem_eval_lec_test_1_mark: parseFloat(document.getElementById('sem_eval_lec_test_1_mark').value),
        sem_eval_lab_test_1_mark: parseFloat(document.getElementById('sem_eval_lab_test_1_mark').value),
        semester_evaluation_mid_mark: parseFloat(document.getElementById('semester_evaluation_mid_mark').value),
        sem_eval_lec_test_2_mark: parseFloat(document.getElementById('sem_eval_lec_test_2_mark').value),
        sem_eval_lab_test_2_mark: parseFloat(document.getElementById('sem_eval_lab_test_2_mark').value),
        semester_evaluation_pre_gtu_mark: parseFloat(document.getElementById('semester_evaluation_pre_gtu_mark').value),
        semester_evaluation_internal_mark: parseFloat(document.getElementById('semester_evaluation_internal_mark').value),
    };
};
// Displays the prediction result
const displayPredictionResult = (data) => {
    document.getElementById('predictedFinalExamMarks').innerText = `Predicted Marks: ${data.predicted_gtu_mark}`;
};

// Shows an error message
const displayError = (message) => {
    document.getElementById('errorDisplay').innerText = message; // Ensure there's an element with id 'errorDisplay'
};
// Initializes the form interaction
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.next').forEach(button => button.addEventListener('click', nextStep));
    document.querySelectorAll('.back').forEach(button => button.addEventListener('click', prevStep));
    document.querySelector('.step[data-step="1"]').style.display = 'block'; // Show the first step
});

document.getElementById('toggleDarkMode').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    
    // Optionally, save the dark mode state in local storage
    if(document.body.classList.contains('dark-mode')){
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
});

// Check local storage for dark mode and apply it on page load
if(localStorage.getItem('darkMode') === 'enabled'){
    document.body.classList.add('dark-mode');
}
function validateNegativeValues() {
    const inputs = document.querySelectorAll('input[type="number"]');
    
    // Create custom alert element
    const alertElement = document.createElement('div');
    alertElement.textContent = 'Please do not enter negative values';
    alertElement.style.position = 'fixed';
    alertElement.style.top = '20px';
    alertElement.style.left = '50%';
    alertElement.style.transform = 'translateX(-50%)';
    alertElement.style.backgroundColor = 'red';
    alertElement.style.padding = '10px';
    alertElement.style.color = 'white';
    alertElement.style.borderRadius = '5px';
    alertElement.style.zIndex = '9999'; // Ensure the alert appears above other elements
    alertElement.style.display = 'none'; // Initially hide the alert

    document.body.appendChild(alertElement);

    inputs.forEach(input => {
        input.addEventListener('input', () => {
            const value = parseFloat(input.value);
            if (value < 0) {
                input.value = '';
                alertElement.style.display = 'block'; // Show the alert
                setTimeout(() => {
                    alertElement.style.display = 'none'; // Hide the alert after some time
                }, 3000); // Adjust the time as needed
            }
        });
    });
}

// Call the function to initialize the validation
validateNegativeValues();
// Call the function to validate negative input values
validateNegativeValues();

