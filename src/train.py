from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from src.dataset import create_dataframe, split_dataframe, CoconutDataset
from src.model import create_model
from src.preprocess import transform


DATA_DIR = Path('data/raw')
MODEL_PATH = Path('models/coconut_resnet18.pth')
BATCH_SIZE = 32
EPOCHS = 5
LEARNING_RATE = 0.001


def validation_accuracy(model, val_loader):

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    return correct / total


def main():

    dataframe = create_dataframe(DATA_DIR)
    train_df, val_df, _ = split_dataframe(dataframe)

    train_dataset = CoconutDataset(train_df,transform)

    val_dataset = CoconutDataset(val_df, transform)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    model = create_model(pretrained=True)

    for parameter in model.parameters():
        parameter.requires_grad = False

    for parameter in model.fc.parameters():
        parameter.requires_grad = True

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(model.fc.parameters(),lr=LEARNING_RATE)

    for epoch in range(EPOCHS):

        model.train()
        running_loss = 0

        for images, labels in train_loader:

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        average_loss = running_loss / len(train_loader)
        accuracy = validation_accuracy(model, val_loader)

        print(
            'Epoch:', epoch + 1,
            'Loss:', round(average_loss, 4),
            'Validation Accuracy:', round(accuracy, 4))

    MODEL_PATH.parent.mkdir(exist_ok=True)

    torch.save(model.state_dict(),MODEL_PATH)

    print('Model saved to:', MODEL_PATH)


if __name__ == '__main__':
    main()
