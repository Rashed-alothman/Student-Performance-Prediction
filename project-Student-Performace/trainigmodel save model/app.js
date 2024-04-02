/*let currentStep = 1; // Initialize the current step to the first step

// Function to change the current step
function changeStep(newStep) {
    const current = document.querySelector(`.step[data-step="${currentStep}"]`);
    const next = document.querySelector(`.step[data-step="${newStep}"]`);

    // Hide current step and show the next step
    if (current) current.style.display = 'none';
    if (next) next.style.display = 'block';

    // Update the current step
    currentStep = newStep;
}

// Function to validate form
function validateForm() {
    // Add your form validation logic here
    // For example, check if all required fields are filled
    // Return true if the form is valid, false otherwise
    const inputs = document.querySelectorAll('.step[data-step="${currentStep}"] input');
    return Array.from(inputs).every(input => input.value !== '');
}

// Function to show loading
function showLoading() {
    // Add your logic to show loading feedback here
    // For example, show a loading spinner or message
    document.getElementById('loading').style.display = 'block';
}

// Function to hide loading
function hideLoading() {
    // Add your logic to hide loading feedback here
    // For example, hide the loading spinner or message
    document.getElementById('loading').style.display = 'none';
}

// Function to move to the next step in the form
function nextStep() {
    // Validate the form before moving to the next step
    if (validateForm()) {
        changeStep(currentStep + 1);
    } else {
        displayError('Please fill all required fields before proceeding.');
    }
}

// Function to move to the previous step in the form
function prevStep() {
    changeStep(currentStep - 1);
}

// Function to handle form submission and prediction
function predict() {
    // Show loading feedback here (e.g., spinner or message)
    showLoading();

    const formData = collectFormData();

    // Sending the prediction request to the Flask app
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading feedback here
        // Display the prediction result
        displayPredictionResult(data);
    })
    .catch(error => {
        console.error('Error:', error);
        // Hide loading feedback here
        displayError('Failed to get prediction');
    });
}

// Collects form data and parses it as needed
function collectFormData() {
    return {
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
}

// Displays prediction result in the UI
function displayPredictionResult(data) {
    document.getElementById('predictedFinalExamMarks').innerText = `Predicted Final Exam Marks: ${data.predicted_gtu_mark}`;
}

// Display an error message in the UI
function displayError(message) {
    document.getElementById('predictedFinalExamMarks').innerText = message;
}


// Initialize the form steps and attach event listeners to "Next" and "Previous" buttons
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.next').forEach(button => {
        button.addEventListener('click', nextStep);
    });
    document.querySelectorAll('.back').forEach(button => {
        button.addEventListener('click', prevStep);
    });
    // Show the first step
    document.querySelector('.step[data-step="1"]').style.display = 'block';
});*/
// old version 1.3
let currentStep = 1; // Initialize the current step to the first step

// Function to change the current step
function changeStep(newStep) {
    const current = document.querySelector(`.step[data-step="${currentStep}"]`);
    const next = document.querySelector(`.step[data-step="${newStep}"]`);

    // Hide current step and show the next step
    if (current) current.style.display = 'none';
    if (next) next.style.display = 'block';

    // Update the current step
    currentStep = newStep;
}

// Function to move to the next step in the form
function nextStep() {
    // Add validation here if needed
    changeStep(currentStep + 1);
}

// Function to move to the previous step in the form
function prevStep() {
    changeStep(currentStep - 1);
}

// Function to handle form submission and prediction
function predict() {
    // Show loading feedback here (e.g., spinner or message)

    const formData = collectFormData();

    // Sending the prediction request to the Flask app
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading feedback here
        // Display the prediction result
        displayPredictionResult(data);
    })
    .catch(error => {
        console.error('Error:', error);
        // Hide loading feedback here
        displayError('Failed to get prediction');
    });
}

// Collects form data and parses it as needed
function collectFormData() {
    return {
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
}

// Displays prediction result in the UI
function displayPredictionResult(data) {
    document.getElementById('predictedFinalExamMarks').innerText = `Predicted Final Exam Marks: ${data.predicted_gtu_mark}`;
}

// Display an error message in the UI
function displayError(message) {
    document.getElementById('predictedFinalExamMarks').innerText = message;
}

// Initialize the form steps and attach event listeners to "Next" and "Previous" buttons
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.next').forEach(button => {
        button.addEventListener('click', nextStep);
    });
    document.querySelectorAll('.back').forEach(button => {
        button.addEventListener('click', prevStep);
    });
    // Show the first step
    document.querySelector('.step[data-step="1"]').style.display = 'block';
});

//old version 1.2
/*let currentStep = 1; // Initialize the current step to the first step

// Function to change the current step
function changeStep(newStep) {
    const current = document.querySelector(`.step[data-step="${currentStep}"]`);
    const next = document.querySelector(`.step[data-step="${newStep}"]`);

    // Hide current step and show the next step
    if (current) current.style.display = 'none';
    if (next) next.style.display = 'block';
    
    // Update the current step
    currentStep = newStep;
}

// Function to move to the next step in the form
function nextStep() {
    // Add validation here if needed
    changeStep(currentStep + 1);
}

// Function to move to the previous step in the form
function prevStep() {
    changeStep(currentStep - 1);
}
// Function to handle form submission and prediction
function predict() {
    const formData = {
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
    
    // Sending the prediction request to the Flask app
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Display the prediction result
        document.getElementById('predictedFinalExamMarks').innerText = `Predicted Final Exam Marks: ${data.predicted_gtu_mark}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('predictedFinalExamMarks').innerText = 'Failed to get prediction';
    });
}


// Add event listeners to "Next" and "Back" buttons
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.next').forEach(button => {
        button.addEventListener('click', nextStep);
    });
    document.querySelectorAll('.back').forEach(button => {
        button.addEventListener('click', prevStep);
    });
    // Initialize the first step as active
    document.querySelector('.step[data-step="1"]').style.display = 'block';
});*/

//old version 1.1
/*function predict() {
    // Collecting input values from the form fields
    var payload = {
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

    // Sending the prediction request to the Flask app
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload) // Convert payload to JSON string
    })
    .then(response => response.json()) // Parsing the JSON response from the server
    .then(data => {
        // Displaying the predicted mark in the specified HTML element
        document.getElementById('predictedFinalExamMarks').innerText = `Predicted Final Exam Marks: ${data.predicted_gtu_mark}`;
        // Resetting the form after successful prediction to clear the fields
        document.getElementById('predictionForm').reset();
    })
    .catch(error => {
        // Error handling if the request fails or the server returns an error
        console.error('Error:', error);
        document.getElementById('predictedFinalExamMarks').innerText = 'Failed to get prediction';
        // Consider resetting the form even on error if you expect users to correct and resubmit.
    });
}
/*function predict() {
    // Collecting input values
    var payload = {
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

    // Sending the prediction request to the Flask app
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // Displaying the predicted mark
        document.getElementById('predictedFinalExamMarks').innerText = `Predicted Final Exam Marks: ${data.predicted_gtu_mark}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('predictedFinalExamMarks').innerText = 'Failed to get prediction';
    });
}

// old version 1.0
/*function predict() {
    // Collect input values
    var semPresentCount = parseFloat(document.getElementById('sem_present_count').value);
    var semAbsentCount = parseFloat(document.getElementById('sem_absent_count').value);
    // Add other variables here based on your model's features

    // Construct the payload
    var payload = {
        sem_present_count: semPresentCount,
        sem_absent_count: semAbsentCount,
        // Add other payload entries here
    };

    // Make the prediction by calling the Flask API
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // Display the prediction
        document.getElementById('predictedFinalExamMarks').innerText = `Predicted Final Exam Marks: ${data.predicted_final_exam_marks}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('predictedFinalExamMarks').innerText = 'Failed to get prediction';
    });
}*/
