function predict() {
    // Construct an object with the input values
    var inputData = {
        semPresentCount: parseFloat(document.getElementById('semPresentCount').value),
        // ... populate with other input values based on their IDs
    };

    // Display input values for debugging
    console.log("Input Values: ", inputData);

    // Make AJAX request to Flask API
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(inputData)
    })
    .then(response => response.json())
    .then(data => {
        // Display the prediction results
        document.getElementById('predictedPerformance').innerText = `Predicted Performance: ${data.predicted_performance}`;
        document.getElementById('passRatio').innerText = `Pass Ratio: ${data.pass_ratio}`;
        document.getElementById('predictedFinalExamMarks').innerText = `Predicted Final Exam Marks: ${data.predicted_final_exam_marks}`;
    })
    .catch(error => console.error('Error:', error));
}
