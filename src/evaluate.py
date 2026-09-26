from pathlib import Path

import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from torch.utils.data import DataLoader

from src.classes import class_names
from src.dataset import create_dataframe, split_dataframe, CoconutDataset
from src.model import load_model
from src.preprocess import transform


DATA_DIR = Path('data/raw')
BATCH_SIZE = 32


def main():

    dataframe = create_dataframe(DATA_DIR)
    _, _, test_df = split_dataframe(dataframe)

    test_dataset = CoconutDataset(
        test_df,
        transform)

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False)

    model = load_model()

    all_predictions = []
    all_labels = []

    with torch.no_grad():

        for images, labels in test_loader:

            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            all_predictions.extend(predicted.tolist())
            all_labels.extend(labels.tolist())

    accuracy = accuracy_score(all_labels,all_predictions)

    print('Test Accuracy:', accuracy)

    print('\nClassification Report:')
    print(classification_report(all_labels,all_predictions,target_names=class_names))

    print('Confusion Matrix:')
    print(confusion_matrix(all_labels, all_predictions))


if __name__ == '__main__':
    main()
