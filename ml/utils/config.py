from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "ml" / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "ml" / "data" / "processed"
MODEL_DIR = BASE_DIR / "ml" / "models" / "saved"

SEQUENCE_LENGTH = 140
NORMAL_CLASS = 1
TEST_SIZE = 0.2
VAL_SIZE = 0.1
RANDOM_SEED = 42

INPUT_DIM = 140
ENCODER_DIMS = [128, 64, 32]
LATENT_DIM = 16
DROPOUT = 0.1

BATCH_SIZE = 64
EPOCHS = 100
LEARNING_RATE = 0.001
EARLY_STOP_PATIENCE = 10

THRESHOLD_PERCENTILE = 95


def create_directories():
    for d in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODEL_DIR]:
        d.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    create_directories()
    print(f"Root: {BASE_DIR}")