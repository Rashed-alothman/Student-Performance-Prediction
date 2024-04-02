// app.js

function predict() {
    // Get input values
    const feature1 = document.getElementById('Study Hours').value;
    const feature2 = document.getElementById('Previous Exam Score').value;

    // Create JSON payload
    const data = {
        feature1: parseFloat(feature1),
        feature2: parseFloat(feature2)
    };

    // Send POST request to Flask backend
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        // Display the prediction result
        document.getElementById('result').innerText = `Prediction: ${result.prediction}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
