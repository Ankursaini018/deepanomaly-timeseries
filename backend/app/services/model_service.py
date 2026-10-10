import numpy as np
import torch

from app.core.config import (
    MODEL_PATH, LSTM_MODEL_PATH, SCALER_MIN_PATH, SCALER_SCALE_PATH,
    THRESHOLD_PATH, LSTM_THRESHOLD_PATH
)
from app.core.model import Autoencoder, LSTMAutoencoder


class ModelService:
    def __init__(self):
        self.device = torch.device("cpu")
        self.models = {}
        self.thresholds = {}
        self.scaler_min = None
        self.scaler_scale = None
        self._loaded = False

    def is_loaded(self) -> bool:
        return self._loaded

    def load(self):
        if self._loaded:
            return

        dense = Autoencoder().to(self.device)
        dense.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
        dense.eval()
        self.models["dense"] = dense
        self.thresholds["dense"] = float(np.load(THRESHOLD_PATH)[0])

        if LSTM_MODEL_PATH.exists():
            lstm = LSTMAutoencoder().to(self.device)
            lstm.load_state_dict(torch.load(LSTM_MODEL_PATH, map_location=self.device))
            lstm.eval()
            self.models["lstm"] = lstm
            self.thresholds["lstm"] = float(np.load(LSTM_THRESHOLD_PATH)[0])

        self.scaler_min = np.load(SCALER_MIN_PATH)
        self.scaler_scale = np.load(SCALER_SCALE_PATH)

        self._loaded = True
        print(f"[ModelService] Loaded models: {list(self.models.keys())}")

    def scale(self, sequence: np.ndarray) -> np.ndarray:
        return (sequence - self.scaler_min) * self.scaler_scale

    def predict(self, sequence: np.ndarray, model_name: str = "dense") -> dict:
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not available. Choose from {list(self.models)}")

        model = self.models[model_name]
        threshold = self.thresholds[model_name]

        scaled = self.scale(sequence).astype(np.float32)
        x = torch.tensor(scaled).unsqueeze(0).to(self.device)

        with torch.no_grad():
            reconstructed = model(x)
            # Error is computed in scaled space, the same space the threshold was fit in
            error = torch.mean((reconstructed - x) ** 2).item()

        # Invert the MinMax transform so the reconstruction is in the same
        # units as the uploaded data and can be plotted against it directly.
        recon_scaled = reconstructed.squeeze(0).numpy()
        recon_raw = recon_scaled / self.scaler_scale + self.scaler_min

        return {
            "model": model_name,
            "reconstruction_error": error,
            "is_anomaly": error > threshold,
            "threshold": threshold,
            "reconstructed": recon_raw.tolist(),
        }


model_service = ModelService()