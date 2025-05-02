// Improved and Organized JavaScript for Handling Form Steps and Predictions

let currentStep = 1; // Track the current form step

// Moves to a specified step
const changeStep = (newStep) => {
    const current = document.querySelector(`.step[data-step="${currentStep}"]`);
    const next = document.querySelector(`.step[data-step="${newStep}"]`);
    
    if (current) current.style.display = 'none';
    if (next) next.style.display = 'block';
    
    currentStep = newStep ;
};

// Advances to the next form step
const nextStep = () => changeStep(currentStep + 1);

// Goes back to the previous form step
const prevStep = () => changeStep(currentStep - 1);

// Submits data for prediction and handles the response
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

