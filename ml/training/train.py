import argparse
import torch
import torch.nn as nn

from ml.data.dataset import get_dataloaders
from ml.models.autoencoder import Autoencoder
from ml.models.lstm_autoencoder import LSTMAutoencoder
from ml.utils.config import MODEL_DIR, EPOCHS, LEARNING_RATE, EARLY_STOP_PATIENCE, RANDOM_SEED

torch.manual_seed(RANDOM_SEED)

MODEL_REGISTRY = {
    "dense": (Autoencoder, "autoencoder_best.pth"),
    "lstm": (LSTMAutoencoder, "lstm_autoencoder_best.pth"),
}


def train(model_name="dense"):
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model '{model_name}'. Choose from {list(MODEL_REGISTRY)}")

    model_cls, filename = MODEL_REGISTRY[model_name]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Model: {model_name} | Device: {device}")

    train_loader, val_loader, _ = get_dataloaders()

    model = model_cls().to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=7
    )

    best_val_loss = float("inf")
    patience_counter = 0
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    save_path = MODEL_DIR / filename

    for epoch in range(1, EPOCHS + 1):
        model.train()
        train_loss = 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            train_loss += loss.item() * x.size(0)
        train_loss /= len(train_loader.dataset)

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                out = model(x)
                val_loss += criterion(out, y).item() * x.size(0)
        val_loss /= len(val_loader.dataset)

        scheduler.step(val_loss)

        if epoch % 5 == 0 or epoch == 1:
            print(f"Epoch {epoch:3d} | Train: {train_loss:.6f} | Val: {val_loss:.6f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            torch.save(model.state_dict(), save_path)
        else:
            patience_counter += 1
            if patience_counter >= EARLY_STOP_PATIENCE:
                print(f"Early stopping at epoch {epoch}")
                break

    print(f"Best val loss: {best_val_loss:.6f}")
    print(f"Saved to {save_path}")
    return best_val_loss


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=list(MODEL_REGISTRY), default="dense")
    args = parser.parse_args()
    train(args.model)