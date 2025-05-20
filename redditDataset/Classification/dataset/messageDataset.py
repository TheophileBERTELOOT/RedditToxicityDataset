from torch.utils.data import Dataset, DataLoader
import pandas as pd

class MessageDataset(Dataset) :
    def __init__(self):
        self.data = pd.read_csv('data/Comments.csv',index_col=0)
        self.data = self.data.dropna(subset=['label'])
        self.labels = self.data['label']
        self.data.drop(['label'],inplace=True)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self,idx):
        return self.data[idx],self.labels[idx]

        