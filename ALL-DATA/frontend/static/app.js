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
            'studyHours': studyHours,
            'prevExamScore': prevExamScore
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display the prediction in the result paragraph
        document.getElementById('result').innerText = `Pass/Fail Prediction: ${data.prediction}`;
    })
    .catch(error => console.error('Error:', error));
}


//function predict() {
    // Get input values
  //  const feature1 = document.getElementById('Study Hours').value;
    //const feature2 = document.getElementById('Previous Exam Score').value;

    // Create JSON payload
    //const data = {
      //  feature1: parseFloat(feature1),
       // feature2: parseFloat(feature2)
   // };

    // Send POST request to Flask backend
    //fetch('http://127.0.0.1:5000/predict', {
      //  method: 'POST',
        //headers: {
         //   'Content-Type': 'application/json',
        //},
        //body: JSON.stringify(data),
    //})
    //.then(response => response.json())
    //.then(result => {
        // Display the prediction result
      //  document.getElementById('result').innerText = `Prediction: ${result.prediction}`;
    //})
    //.catch(error => {
     //   console.error('Error:', error);
    //});
//}
