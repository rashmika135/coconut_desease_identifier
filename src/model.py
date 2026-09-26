from pathlib import Path

import torch
import torch.nn as nn
from torchvision import models

from src.classes import class_names
from src.preprocess import transform


project_root = Path(__file__).resolve().parents[1]
model_path = project_root / 'models' / 'coconut_resnet18.pth'

loaded_model = None


def create_model(pretrained=False):

    if pretrained:
        weights = models.ResNet18_Weights.DEFAULT
    else:
        weights = None

    model = models.resnet18(weights=weights)

    model.fc = nn.Linear(
        model.fc.in_features,
        len(class_names))

    return model


def load_model():

    if not model_path.exists():
        raise FileNotFoundError(
            f'Model file not found: {model_path}')

    model = create_model(pretrained=False)

    state_dict = torch.load(model_path,map_location='cpu',weights_only=True)

    model.load_state_dict(state_dict)
    model.eval()

    return model


def get_model():

    global loaded_model

    if loaded_model is None:
        loaded_model = load_model()

    return loaded_model


def predict_image(image):

    model = get_model()

    image = image.convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)

    with torch.no_grad():

        output = model(image)
        probabilities = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    predicted_class = class_names[predicted.item()]

    return predicted_class, confidence.item()