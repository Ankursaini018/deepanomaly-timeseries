import numpy as np
import pandas as pd

from ml.utils.config import RAW_DATA_DIR, NORMAL_CLASS, BASE_DIR, RANDOM_SEED

OUT_DIR = BASE_DIR / "docs" / "sample_data"


def main(n_normal=10, n_anomaly=10):
    frames = [
        pd.read_csv(RAW_DATA_DIR / name, sep=r"\s+", header=None)
        for name in ("ECG5000_TRAIN.txt", "ECG5000_TEST.txt")
    ]
    df = pd.concat(frames, ignore_index=True)
    labels = df.iloc[:, 0].astype(int).to_numpy()
    seqs = df.iloc[:, 1:].to_numpy(dtype=np.float32)

    rng = np.random.default_rng(RANDOM_SEED)
    normal_idx = rng.choice(np.where(labels == NORMAL_CLASS)[0], n_normal, replace=False)
    anomaly_idx = rng.choice(np.where(labels != NORMAL_CLASS)[0], n_anomaly, replace=False)

    idx = rng.permutation(np.concatenate([normal_idx, anomaly_idx]))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    np.savetxt(OUT_DIR / "demo_sequences.csv", seqs[idx], delimiter=",")
    pd.Series((labels[idx] != NORMAL_CLASS).astype(int)).to_csv(
        OUT_DIR / "demo_labels.csv", index=False, header=["is_anomaly"]
    )
    print(f"Wrote {len(idx)} raw sequences ({n_anomaly} anomalous) to {OUT_DIR}")


if __name__ == "__main__":
    main()