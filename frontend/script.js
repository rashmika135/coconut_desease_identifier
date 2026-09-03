const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const predictButton = document.getElementById('predictButton');
const result = document.getElementById('result');


imageInput.addEventListener('change', function () {
    const file = imageInput.files[0];

    if (!file) {
        return;}

    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';

    predictButton.disabled = false;
    result.innerHTML = '';});


predictButton.addEventListener('click', async function () {
    const file = imageInput.files[0];

    if (!file) {
        return;}

    predictButton.disabled = true;
    predictButton.textContent = 'Predicting...';
    result.innerHTML = '';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData});

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Prediction failed.');}

        const confidence = (data.confidence * 100).toFixed(2);

        result.innerHTML = `
            <strong>Prediction:</strong> ${data.prediction}
            <br>
            <strong>Confidence:</strong> ${confidence}%`;

    } catch (error) {
        result.textContent = error.message;}

    predictButton.disabled = false;
    predictButton.textContent = 'Predict';});