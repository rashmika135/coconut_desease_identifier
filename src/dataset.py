from pathlib import Path
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset

folder_map = {
    'Healthy_Leaves': 'Healthy',
    'CCI_Leaflets': 'CCI',
    'WCLWD_Yellowing': 'WCLWD_Yellowing',
    'WCLWD_Flaccidity': 'WCLWD_Flaccidity',
    'WCLWD_DryingofLeaflets': 'WCLWD_Drying'}

image_extensions = {
    '.jpg',
    '.jpeg',
    '.png',
    '.bmp',
    '.webp'}

def create_dataframe(data_dir):

    data_dir = Path(data_dir)

    image_paths = []
    labels = []

    for folder_name, label in folder_map.items():

        folder_path = data_dir / folder_name
        nested_folder = folder_path / folder_name

        if nested_folder.exists():
            folder_path = nested_folder

        if not folder_path.exists():
            raise FileNotFoundError(
                f'Dataset folder not found: {folder_path}')

        for image_path in folder_path.iterdir():

            if image_path.suffix.lower() in image_extensions:
                image_paths.append(str(image_path))
                labels.append(label)

    dataframe = pd.DataFrame({
        'image_path': image_paths,
        'label': labels})

    return dataframe

def split_dataframe(dataframe):

    train_df, temp_df = train_test_split(
        dataframe,
        test_size=0.3,
        stratify=dataframe['label'],
        random_state=42)

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        stratify=temp_df['label'],
        random_state=42)

    return train_df, val_df, test_df

class CoconutDataset(Dataset):

    def __init__(self, dataframe, transform):
        self.dataframe = dataframe.reset_index(drop=True)
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, index):

        image_path = self.dataframe.iloc[index]['image_path']
        label = self.dataframe.iloc[index]['label']

        image = Image.open(image_path).convert('RGB')
        image = self.transform(image)

        label = label_map[label]

        return image, label

