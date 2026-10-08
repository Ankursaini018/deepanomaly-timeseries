import argparse
import numpy as np
import torch
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)

from ml.data.dataset import get_dataloaders
from ml.models.autoencoder import Autoencoder
from ml.models.lstm_autoencoder import LSTMAutoencoder
from ml.utils.config import MODEL_DIR, THRESHOLD_PERCENTILE

MODEL_REGISTRY = {
    "dense": (Autoencoder, "autoencoder_best.pth", "threshold.npy"),
    "lstm": (LSTMAutoencoder, "lstm_autoencoder_best.pth", "lstm_threshold.npy"),
}


def get_reconstruction_errors(model, loader, device):
    model.eval()
    errors, labels = [], []
    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            out = model(x)
            err = torch.mean((out - x) ** 2, dim=1).cpu().numpy()
            errors.extend(err)
            labels.extend(y.numpy() if y.dim() > 0 else [y.item()])
    return np.array(errors), np.array(labels)


def evaluate(model_name="dense", save_threshold=True):
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model '{model_name}'")

    model_cls, weight_file, threshold_file = MODEL_REGISTRY[model_name]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = model_cls().to(device)
    model.load_state_dict(torch.load(MODEL_DIR / weight_file, map_location=device))

    train_loader, val_loader, test_loader = get_dataloaders()

    val_errors, _ = get_reconstruction_errors(model, val_loader, device)
    threshold = np.percentile(val_errors, THRESHOLD_PERCENTILE)

    test_errors, y_true = get_reconstruction_errors(model, test_loader, device)
    y_pred = (test_errors > threshold).astype(int)

    metrics = {
        "model": model_name,
        "threshold": threshold,
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, test_errors),
    }

    print(f"\n--- {model_name.upper()} ---")
    for k, v in metrics.items():
        if k != "model":
            print(f"{k:>10}: {v:.4f}" if isinstance(v, float) else f"{k:>10}: {v}")
    print("Confusion matrix:")
    print(confusion_matrix(y_true, y_pred))

    if save_threshold:
        np.save(MODEL_DIR / threshold_file, np.array([threshold]))

    return metrics


def compare_all():
    results = [evaluate(name) for name in MODEL_REGISTRY]

    print("\n" + "=" * 50)
    print("COMPARISON")
    print("=" * 50)
    print(f"{'Model':<10}{'Precision':<12}{'Recall':<10}{'F1':<10}{'ROC-AUC':<10}")
    for r in results:
        print(f"{r['model']:<10}{r['precision']:<12.4f}{r['recall']:<10.4f}{r['f1']:<10.4f}{r['roc_auc']:<10.4f}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=list(MODEL_REGISTRY) + ["all"], default="all")
    args = parser.parse_args()

    if args.model == "all":
        compare_all()
    else:
        evaluate(args.model)