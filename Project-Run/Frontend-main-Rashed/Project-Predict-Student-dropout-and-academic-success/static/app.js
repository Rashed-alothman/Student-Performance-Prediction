document.addEventListener("DOMContentLoaded", function () {
  const manualEntryForm = document.getElementById("manual-entry-form");
  const manualEntryButton = document.getElementById("manualEntryButton");
  const csvUploadForm = document.getElementById("csv-upload-form");
  const predictionResult = document.getElementById("predictionResult");
  const csvFileInput = document.getElementById("csvFile");
  const darkModeToggle = document.getElementById("darkModeToggle");
  const waveBackground = document.querySelector(".wave-background");

  // Function to handle form submission for JSON data
  function handleJSONFormSubmit(e, url, jsonData) {
    e.preventDefault();
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonData,
    })
      .then((response) => response.json())
      .then((data) => {
        predictionResult.textContent = `Prediction Result: ${data.result}`;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  // Function to handle form submission for FormData (File upload)
  function handleFileFormSubmit(e, url, formData) {
    e.preventDefault();
    fetch(url, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Assuming the server responds with an array of predictions
        predictionResult.innerHTML = "<h3>Predictions:</h3>";
        data.forEach((pred, index) => {
          const result = pred === 1 ? "Success (Pass)" : "Dropout (Fail)";
          predictionResult.innerHTML += `Prediction ${index + 1}: ${pred}<br>`;
        });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  manualEntryButton.addEventListener("click", function () {
    // Toggle the form's display property
    manualEntryForm.style.display =
      manualEntryForm.style.display === "none" ? "block" : "none";
  });

  // Handle manual data entry form submission
  manualEntryForm.addEventListener("submit", function (e) {
    const jsonData = JSON.stringify(
      Object.fromEntries(new FormData(manualEntryForm).entries())
    );
    handleJSONFormSubmit(e, "/predict_manual", jsonData);
  });

  // Handle CSV file upload form submission
  csvUploadForm.addEventListener("submit", function (e) {
    const formData = new FormData();
    if (csvFileInput.files.length > 0) {
      formData.append("file", csvFileInput.files[0]);
      handleFileFormSubmit(e, "/predict_csv", formData);
    } else {
      alert("Please select a file to upload.");
    }
  });

  // Toggle dark mode
  darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem(
      "darkMode",
      document.body.classList.contains("dark-mode") ? "enabled" : "disabled"
    );
    updateWaveColors();
  });

  // Update wave colors based on the theme
  function updateWaveColors() {
    waveBackground.style.background = document.body.classList.contains(
      "dark-mode"
    )
      ? "linear-gradient(60deg, #292e49, #536976)" // Dark mode wave colors
      : "linear-gradient(60deg, #6d5dfc, #c3a0f7)"; // Light mode wave colors
  }

  // Apply dark mode from localStorage
  if (localStorage.getItem("darkMode") === "enabled") {
    document.body.classList.add("dark-mode");
  }

  updateWaveColors(); // Ensure wave colors are set on page load
});

// Function to show the manual entry form
function showManualEntryForm() {
  document.getElementById("manual-entry-form").style.display = "block";
  document.getElementById("csv-upload-form").style.display = "none";
}
/* old version
document.addEventListener("DOMContentLoaded", function () {

  // Handle manual data entry form submission
  document
    .getElementById("manual-entry-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData(this);
      const data = Object.fromEntries(formData.entries());

      fetch("/predict_manual", {
        // Adjust '/predict_manual' to your Flask route
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((prediction) => {
          document.getElementById(
            "predictionResult"
          ).textContent = `Manual Prediction Result: ${prediction.result}`;
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });

  // Handle CSV file upload form submission
  document
    .getElementById("csv-upload-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData();
      const fileInput = document.getElementById("csvFile");
      if (fileInput.files.length > 0) {
        formData.append("csvFile", fileInput.files[0]);
      }

      fetch("/predict_csv", {
        // Adjust '/predict_csv' to your Flask route
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((prediction) => {
          document.getElementById(
            "predictionResult"
          ).textContent = `CSV Prediction Result: ${prediction.result}`;
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });

  // Optional: Implement Dark Mode Toggle
  const toggleDarkMode = document.getElementById("darkModeToggle");
  toggleDarkMode.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    // Optionally, save the dark mode state in localStorage
    localStorage.setItem(
      "darkMode",
      document.body.classList.contains("dark-mode") ? "enabled" : "disabled"
    );
    // Update wave colors for the theme
    updateWaveColors();
  });
  // Update wave colors based on the theme
  function updateWaveColors() {
    const waveBackground = document.querySelector(".wave-background");
    if (document.body.classList.contains("dark-mode")) {
      waveBackground.style.background =
        "linear-gradient(60deg, #292e49, #536976)"; // Dark mode wave colors
    } else {
      waveBackground.style.background =
        "linear-gradient(60deg, #6d5dfc, #c3a0f7)"; // Light mode wave colors
    }
  }
  // Apply dark mode from localStorage
  if (localStorage.getItem("darkMode") === "enabled") {
    document.body.classList.add("dark-mode");
  }
});
// Function to show the manual entry form
function showManualEntryForm() {
  document.getElementById("manual-entry-form").style.display = "block";
  document.getElementById("csv-upload-form").style.display = "none";
}
updateWaveColors(); // Ensure wave colors are set on page load*/
