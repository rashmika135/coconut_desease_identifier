const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const predictButton = document.getElementById('predictButton');
const fileName = document.getElementById('fileName');
const result = document.getElementById('result');
const predictionText = document.getElementById('predictionText');
const confidenceText = document.getElementById('confidenceText');
const confidenceFill = document.getElementById('confidenceFill');
const meaningText = document.getElementById('meaningText');
const causeText = document.getElementById('causeText');
const actionText = document.getElementById('actionText');

const displayNames = {
    Healthy: 'Healthy Leaf',
    CCI: 'Coconut Caterpillar Infestation',
    WCLWD_Yellowing: 'WCLWD - Yellowing',
    WCLWD_Flaccidity: 'WCLWD - Flaccidity',
    WCLWD_Drying: 'WCLWD - Drying'
};

const conditionInfo = {
    Healthy: {
        meaning: 'No visible signs of the conditions recognized by this model were detected.',
        cause: 'No disease or pest cause is indicated by this prediction.',
        action: 'Continue regular monitoring and keep the palm well maintained. If unusual symptoms appear later, check the palm again or seek agricultural advice.'
    },

    CCI: {
        meaning: 'The leaf shows signs that are consistent with coconut caterpillar damage.',
        cause: 'Coconut Caterpillar Infestation is caused by caterpillars feeding on coconut leaf tissue.',
        action: 'Inspect nearby leaves for similar damage and consult an agricultural officer for suitable pest management advice.'
    },

    WCLWD_Yellowing: {
        meaning: 'The leaf shows unusual yellowing associated with Weligama Coconut Leaf Wilt Disease.',
        cause: 'WCLWD is associated with a phytoplasma infection in coconut palms.',
        action: 'Monitor nearby palms for similar symptoms, avoid moving planting material from affected areas, and seek advice from a coconut or agricultural officer.'
    },

    WCLWD_Flaccidity: {
        meaning: 'The leaflets lose their normal firm shape, become flatter and may bend downward.',
        cause: 'Flaccidity is an early symptom associated with Weligama Coconut Leaf Wilt Disease, which is linked to phytoplasma infection.',
        action: 'Check nearby palms for similar symptoms, continue monitoring the affected palm, and contact a coconut or agricultural officer for field advice.'
    },

    WCLWD_Drying: {
        meaning: 'The leaf shows drying symptoms that can occur as Weligama Coconut Leaf Wilt Disease progresses.',
        cause: 'WCLWD is associated with phytoplasma infection, and affected leaflets may begin drying from their margins.',
        action: 'Record the symptoms, inspect surrounding palms, and get guidance from a coconut or agricultural officer as soon as possible.'
    }
};

imageInput.addEventListener('change', function () {
    const file = imageInput.files[0];

    result.style.display = 'none';

    if (!file) {
        preview.style.display = 'none';
        fileName.textContent = 'No image selected';
        predictButton.disabled = true;
        return;
    }

    fileName.textContent = file.name;
    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';
    predictButton.disabled = false;
});

predictButton.addEventListener('click', async function () {
    const file = imageInput.files[0];

    if (!file) {
        return;
    }

    predictButton.disabled = true;
    predictButton.textContent = 'Analyzing...';
    result.style.display = 'none';
    result.classList.remove('error');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Prediction failed.');
        }

        const confidence = (data.confidence * 100).toFixed(2);
        const name = displayNames[data.prediction] || data.prediction;
        const info = conditionInfo[data.prediction];

        predictionText.textContent = name;
        confidenceText.textContent = `${confidence}%`;
        confidenceFill.style.width = `${confidence}%`;

        if (info) {
            meaningText.textContent = info.meaning;
            causeText.textContent = info.cause;
            actionText.textContent = info.action;
        } else {
            meaningText.textContent = 'No additional information is available for this result.';
            causeText.textContent = 'Unknown.';
            actionText.textContent = 'Please inspect the leaf again or consult an agricultural expert.';
        }

        result.style.display = 'block';

    } catch (error) {
        predictionText.textContent = 'Prediction failed';
        confidenceText.textContent = '';
        confidenceFill.style.width = '0%';
        meaningText.textContent = error.message;
        causeText.textContent = '';
        actionText.textContent = '';
        result.classList.add('error');
        result.style.display = 'block';
    }

    predictButton.disabled = false;
    predictButton.textContent = 'Analyze Leaf';
});
