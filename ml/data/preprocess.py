import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from ml.utils.config import (
    RAW_DATA_DIR, PROCESSED_DATA_DIR, NORMAL_CLASS,
    TEST_SIZE, VAL_SIZE, RANDOM_SEED
)


def load_raw():
    train = pd.read_csv(RAW_DATA_DIR / "ECG5000_TRAIN.txt", sep=r"\s+", header=None)
    test = pd.read_csv(RAW_DATA_DIR / "ECG5000_TEST.txt", sep=r"\s+", header=None)
    df = pd.concat([train, test], ignore_index=True)

    labels = df.iloc[:, 0].astype(int).values
    sequences = df.iloc[:, 1:].values.astype(np.float32)
    return sequences, labels


def to_binary(labels):
    return (labels != NORMAL_CLASS).astype(int)


def preprocess():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    sequences, labels = load_raw()
    binary = to_binary(labels)

    normal = sequences[binary == 0]
    anomaly = sequences[binary == 1]

    # Train/val: normal only. Test: normal + anomaly.
    normal_train, normal_test = train_test_split(
        normal, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )
    normal_train, normal_val = train_test_split(
        normal_train, test_size=VAL_SIZE, random_state=RANDOM_SEED
    )

    # Fit scaler on train only — no leakage
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(normal_train).astype(np.float32)
    X_val = scaler.transform(normal_val).astype(np.float32)
    normal_test_s = scaler.transform(normal_test).astype(np.float32)
    anomaly_s = scaler.transform(anomaly).astype(np.float32)

    X_test = np.vstack([normal_test_s, anomaly_s])
    y_test = np.concatenate([
        np.zeros(len(normal_test_s)), np.ones(len(anomaly_s))
    ])

    # Shuffle test set
    rng = np.random.default_rng(RANDOM_SEED)
    idx = rng.permutation(len(X_test))
    X_test, y_test = X_test[idx], y_test[idx]

    np.save(PROCESSED_DATA_DIR / "X_train.npy", X_train)
    np.save(PROCESSED_DATA_DIR / "X_val.npy", X_val)
    np.save(PROCESSED_DATA_DIR / "X_test.npy", X_test)
    np.save(PROCESSED_DATA_DIR / "y_test.npy", y_test)
    np.save(PROCESSED_DATA_DIR / "scaler_min.npy", scaler.data_min_)
    np.save(PROCESSED_DATA_DIR / "scaler_scale.npy", scaler.scale_)

    print(f"Train: {X_train.shape} | Val: {X_val.shape} | Test: {X_test.shape}")
    print(f"Test anomalies: {int(y_test.sum())}/{len(y_test)}")


if __name__ == "__main__":
    preprocess()