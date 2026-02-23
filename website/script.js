function analyzeSoil() {
    const resultBox = document.getElementById("analysis-result");
    resultBox.innerHTML = "Analyzing soil image... ⏳";
  
    fetch("http://localhost:5000/predict_soil")
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          resultBox.innerHTML = `<span style="color:red;">Error: ${data.error}</span>`;
        } else {
          const npk = data.NPK;
          const fertilizer = data.recommended_fertilizer;
  
          resultBox.innerHTML = `
            <h3>Analysis Results:</h3>
            <p><strong>Predicted pH:</strong> ${data.ph_value}</p>
            <p><strong>Nitrogen (N):</strong> ${npk["Nitrogen (N)"]}</p>
            <p><strong>Phosphorus (P):</strong> ${npk["Phosphorus (P)"]}</p>
            <p><strong>Potassium (K):</strong> ${npk["Potassium (K)"]}</p>
            <p><strong>Recommended Crop:</strong> ${npk["Crop(C)"]}</p>
            <p><strong>Recommended Fertilizer:</strong> ${fertilizer}</p>
          `;
        }
      })
      .catch(error => {
        resultBox.innerHTML = `<span style="color:red;">Request failed: ${error}</span>`;
      });
  }

  // Add captureAnalyze function to handle image + prediction display
  function captureAnalyze() {
    const loading = document.getElementById('analysisLoading');
    const resultDiv = document.getElementById('analysisResult');
    const imgEl = document.getElementById('analysisImage');
    const phEl = document.getElementById('phValue');
    const npkEl = document.getElementById('npkValues');
    const fertEl = document.getElementById('fertilizer');
  
    loading.style.display = 'block';
    resultDiv.style.display = 'none';
  
    fetch('http://localhost:5000/predict_soil')
      .then(res => res.json())
      .then(data => {
        loading.style.display = 'none';
        if (data.error) {
          alert('Error: ' + data.error);
          return;
        }
        imgEl.src = 'http://localhost:5000/captured_images/latest.jpg';
        phEl.textContent = `pH Value: ${data.ph_value.toFixed(2)}`;
        const npk = data.NPK;
        npkEl.textContent = `N: ${npk['Nitrogen (N)']}, P: ${npk['Phosphorus (P)']}, K: ${npk['Potassium (K)']}. Crop: ${npk['Crop(C)']}`;
        fertEl.textContent = 'Recommended Fertilizer: ' + data.recommended_fertilizer;
        resultDiv.style.display = 'block';
      })
      .catch(err => {
        loading.style.display = 'none';
        alert('Failed to analyze soil. Make sure the backend is running.');
        console.error(err);
      });
  }
