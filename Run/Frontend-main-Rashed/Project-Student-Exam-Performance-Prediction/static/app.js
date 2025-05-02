// app.js
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