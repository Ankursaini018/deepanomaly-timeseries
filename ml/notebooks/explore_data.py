import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ml.utils.config import RAW_DATA_DIR, NORMAL_CLASS, BASE_DIR

PLOTS_DIR = BASE_DIR / "docs" / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    train = pd.read_csv(RAW_DATA_DIR / "ECG5000_TRAIN.txt", sep=r"\s+", header=None)
    test = pd.read_csv(RAW_DATA_DIR / "ECG5000_TEST.txt", sep=r"\s+", header=None)
    df = pd.concat([train, test], ignore_index=True)
    labels = df.iloc[:, 0].astype(int).values
    sequences = df.iloc[:, 1:].values.astype(float)
    return sequences, labels


def plot_class_distribution(labels):
    fig, ax = plt.subplots(figsize=(8, 5))
    classes, counts = np.unique(labels, return_counts=True)
    colors = ["#2E86AB" if c == NORMAL_CLASS else "#E63946" for c in classes]
    ax.bar(classes, counts, color=colors, edgecolor="black")
    ax.set_xlabel("Class")
    ax.set_ylabel("Count")
    ax.set_title("Class Distribution")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "class_distribution.png", dpi=150)
    plt.close()


def plot_average_patterns(sequences, labels):
    fig, ax = plt.subplots(figsize=(11, 6))
    normal = sequences[labels == NORMAL_CLASS]
    anomaly = sequences[labels != NORMAL_CLASS]
    x = np.arange(sequences.shape[1])

    ax.plot(x, normal.mean(axis=0), color="#2E86AB", label="Normal", linewidth=2)
    ax.plot(x, anomaly.mean(axis=0), color="#E63946", label="Anomalous", linewidth=2)
    ax.legend()
    ax.set_title("Average Heartbeat Pattern")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "average_pattern.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    sequences, labels = load_data()
    print(f"Total: {len(sequences)} | Normal: {(labels==NORMAL_CLASS).sum()} | Anomaly: {(labels!=NORMAL_CLASS).sum()}")
    plot_class_distribution(labels)
    plot_average_patterns(sequences, labels)
    print(f"Plots saved to {PLOTS_DIR}")