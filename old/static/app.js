function predict() {
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

// old version 
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
