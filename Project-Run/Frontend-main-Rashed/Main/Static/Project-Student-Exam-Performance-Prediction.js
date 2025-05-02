// Function to create and display custom alerts
function showAlert(message) {
    var alertDiv = document.createElement('div');
    alertDiv.textContent = message;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '-50px'; // Set top to a negative value to position above the page
    alertDiv.style.left = '50%';
    alertDiv.style.transform = 'translateX(-50%)';
    alertDiv.style.padding = '20px';
    alertDiv.style.backgroundColor = 'red';
    alertDiv.style.color = 'white';
    alertDiv.style.borderRadius = '5px';
    alertDiv.style.zIndex = '9999';
    document.body.appendChild(alertDiv);

    // Animate alert to slide down
    setTimeout(function() {
        alertDiv.style.top = '20px'; // Set top to desired position
    }, 100);

    // Remove the alert after 3 seconds
    setTimeout(function() {
        alertDiv.style.top = '-50px'; // Slide alert back up
        setTimeout(function() {
            document.body.removeChild(alertDiv); // Remove alert after sliding up
        }, 500); // Wait for animation to complete before removing
    }, 3000);
}


function predict() {
    // Get input values
    var studyHours = parseFloat(document.getElementById('studyHours').value);
    var prevExamScore = parseFloat(document.getElementById('prevExamScore').value);
    const totalPoints = prevExamScore;

    if (totalPoints > 100) {
        showAlert('Please do not enter points exceeding 100.');
        return;
    }
    // Display input values
    document.getElementById('inputValues').innerText = `Input Values: Study Hours - ${studyHours}, Previous Exam Score - ${prevExamScore}`;

    // Make AJAX request to Flask API
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'studyHours': studyHours,  // Update key to match Flask app
            'prevExamScore': prevExamScore  // Update key to match Flask app
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display the prediction in the result paragraph
        document.getElementById('result').innerText = `Pass/Fail Prediction: ${data.result}`;
    })
    .catch(error => console.error('Error:', error));
}

// Function to validate negative input values
function validateNegativeValues() {
    const inputs = document.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            const value = parseFloat(input.value);
            if (value < 0) {
                input.value = '';
                showAlert('Please do not enter negative values.');
            }
        });
    });
}

// Call the function to validate negative input values
validateNegativeValues();



/* app.js older versions
function predict() {
    // Get input values
    var studyHours = parseFloat(document.getElementById('studyHours').value);
    var prevExamScore = parseFloat(document.getElementById('prevExamScore').value);

    // Display input values
    document.getElementById('inputValues').innerText = `Input Values: Study Hours - ${studyHours}, Previous Exam Score - ${prevExamScore}`;

    // Make AJAX request to Flask API
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'study_hours': studyHours,  // Update key to match Flask app
            'prev_exam_score': prevExamScore  // Update key to match Flask app
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display the prediction in the result paragraph
        document.getElementById('result').innerText = `Pass/Fail Prediction: ${data.result}`;
    })
    .catch(error => console.error('Error:', error));
}
*/