"""
Evaluate every registered model on the held-out test set and write:
  docs/results/metrics.json        machine-readable numbers
  docs/results/results.md          table to paste into the README
  docs/plots/error_distribution.png
  docs/plots/roc_curves.png
"""

import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import (
    average_precision_score, f1_score, precision_score,
    recall_score, roc_auc_score, roc_curve,
)

from ml.data.dataset import get_dataloaders
from ml.evaluation.evaluate import MODEL_REGISTRY, get_reconstruction_errors
from ml.utils.config import BASE_DIR, MODEL_DIR, THRESHOLD_PERCENTILE

RESULTS_DIR = BASE_DIR / "docs" / "results"
PLOTS_DIR = BASE_DIR / "docs" / "plots"
LABELS = {"dense": "Dense Autoencoder", "lstm": "LSTM Autoencoder"}
COLORS = {"dense": "#ef4444", "lstm": "#22c55e"}


def run():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cpu")
    _, val_loader, test_loader = get_dataloaders()

    metrics, test_errs, y_true = {}, {}, None

    for name, (cls, weights, _) in MODEL_REGISTRY.items():
        model = cls().to(device)
        model.load_state_dict(torch.load(MODEL_DIR / weights, map_location=device))

        val_err, _ = get_reconstruction_errors(model, val_loader, device)
        err, y = get_reconstruction_errors(model, test_loader, device)
        thr = float(np.percentile(val_err, THRESHOLD_PERCENTILE))
        pred = (err > thr).astype(int)

        metrics[name] = {
            "threshold": thr,
            "precision": float(precision_score(y, pred)),
            "recall": float(recall_score(y, pred)),
            "f1": float(f1_score(y, pred)),
            "roc_auc": float(roc_auc_score(y, err)),
            "pr_auc": float(average_precision_score(y, err)),
            "false_positive_rate": float(((pred == 1) & (y == 0)).sum() / (y == 0).sum()),
        }
        test_errs[name], y_true = err, y

    (RESULTS_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))

    lines = [
        "| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC | FPR |",
        "|---|---|---|---|---|---|---|",
    ]
    for n, m in metrics.items():
        lines.append(
            f"| {LABELS[n]} | {m['precision']:.3f} | {m['recall']:.3f} | {m['f1']:.3f} "
            f"| {m['roc_auc']:.3f} | {m['pr_auc']:.3f} | {m['false_positive_rate']:.3f} |"
        )
    (RESULTS_DIR / "results.md").write_text("\n".join(lines) + "\n")

    # Error distributions: the separation between the two histograms IS the detector
    fig, axes = plt.subplots(1, len(test_errs), figsize=(6 * len(test_errs), 4.5))
    axes = np.atleast_1d(axes)
    for ax, (n, err) in zip(axes, test_errs.items()):
        hi = np.percentile(err, 99)
        bins = np.linspace(0, hi, 50)
        ax.hist(err[y_true == 0], bins=bins, alpha=0.65, color="#2E86AB", label="Normal")
        ax.hist(err[y_true == 1], bins=bins, alpha=0.65, color="#E63946", label="Anomaly")
        ax.axvline(metrics[n]["threshold"], color="black", ls="--", label="Threshold")
        ax.set_title(LABELS[n])
        ax.set_xlabel("Reconstruction error (MSE)")
        ax.set_ylabel("Count")
        ax.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "error_distribution.png", dpi=150)
    plt.close()

    plt.figure(figsize=(6, 5))
    for n, err in test_errs.items():
        fpr, tpr, _ = roc_curve(y_true, err)
        plt.plot(fpr, tpr, color=COLORS[n], lw=2,
                 label=f"{LABELS[n]} (AUC {metrics[n]['roc_auc']:.3f})")
    plt.plot([0, 1], [0, 1], "k--", alpha=0.4)
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.title("ROC curves on held-out test set")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "roc_curves.png", dpi=150)
    plt.close()

    print((RESULTS_DIR / "results.md").read_text())


if __name__ == "__main__":
    run()