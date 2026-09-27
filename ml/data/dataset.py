import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

from ml.utils.config import PROCESSED_DATA_DIR, BATCH_SIZE


class TimeSeriesDataset(Dataset):
    def __init__(self, sequences, labels=None):
        self.sequences = torch.tensor(sequences, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32) if labels is not None else None

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        seq = self.sequences[idx]
        if self.labels is not None:
            return seq, self.labels[idx]
        return seq, seq  # autoencoder: input == target


def get_dataloaders(batch_size=BATCH_SIZE):
    X_train = np.load(PROCESSED_DATA_DIR / "X_train.npy")
    X_val = np.load(PROCESSED_DATA_DIR / "X_val.npy")
    X_test = np.load(PROCESSED_DATA_DIR / "X_test.npy")
    y_test = np.load(PROCESSED_DATA_DIR / "y_test.npy")

    train_loader = DataLoader(TimeSeriesDataset(X_train), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(TimeSeriesDataset(X_val), batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(TimeSeriesDataset(X_test, y_test), batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader


if __name__ == "__main__":
    train_loader, val_loader, test_loader = get_dataloaders()
    x, y = next(iter(train_loader))
    print(f"Train batches: {len(train_loader)} | Sample shape: {x.shape}")