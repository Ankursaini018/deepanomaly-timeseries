import numpy as np
import torch
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

from ml.data.dataset import get_dataloaders
from ml.models.autoencoder import Autoencoder
from ml.utils.config import MODEL_DIR, THRESHOLD_PERCENTILE


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


def evaluate():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = Autoencoder().to(device)
    model.load_state_dict(torch.load(MODEL_DIR / "autoencoder_best.pth", map_location=device))

    train_loader, val_loader, test_loader = get_dataloaders()

    # Threshold from val set (normal-only)
    val_errors, _ = get_reconstruction_errors(model, val_loader, device)
    threshold = np.percentile(val_errors, THRESHOLD_PERCENTILE)
    print(f"Threshold ({THRESHOLD_PERCENTILE}th percentile of val errors): {threshold:.6f}")
    np.save(
    MODEL_DIR.parent.parent / "models" / "saved" / "threshold.npy",
    np.array([threshold], dtype=np.float32)
)

    # Evaluate on test set
    test_errors, y_true = get_reconstruction_errors(model, test_loader, device)
    y_pred = (test_errors > threshold).astype(int)

    print("\n--- Metrics ---")
    print(f"Precision: {precision_score(y_true, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_true, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_true, y_pred):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_true, test_errors):.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    print("\n" + classification_report(y_true, y_pred, target_names=["Normal", "Anomaly"]))

    return {
        "threshold": threshold,
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, test_errors),
    }


if __name__ == "__main__":
    evaluate()