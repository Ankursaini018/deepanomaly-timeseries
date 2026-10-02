import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "autoencoder_best.pth"
SCALER_MIN_PATH = ARTIFACTS_DIR / "scaler_min.npy"
SCALER_SCALE_PATH = ARTIFACTS_DIR / "scaler_scale.npy"
THRESHOLD_PATH = ARTIFACTS_DIR / "threshold.npy"

INPUT_DIM = 140
ENCODER_DIMS = [128, 64, 32]
LATENT_DIM = 16

# Comma-separated list, e.g. "https://myapp.up.railway.app,http://localhost:5173"
_default_origins = "http://localhost:5173,http://127.0.0.1:5173"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", _default_origins).split(",")