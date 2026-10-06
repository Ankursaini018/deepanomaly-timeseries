import numpy as np
import torch

from app.core.config import (
    MODEL_PATH,
    SCALER_MIN_PATH,
    SCALER_SCALE_PATH,
    THRESHOLD_PATH,
)
from app.core.model import Autoencoder


class ModelService:
    """
    Loads model + scaler + threshold once at startup.
    Avoids reloading weights from disk on every request.
    """

    def __init__(self):
        self.device = torch.device("cpu")
        self.model = None
        self.scaler_min = None
        self.scaler_scale = None
        self.threshold = None
        self._loaded = False

    def load(self):
        if self._loaded:
            return

        for path in (
            MODEL_PATH,
            SCALER_MIN_PATH,
            SCALER_SCALE_PATH,
            THRESHOLD_PATH,
        ):
            if not path.exists():
                raise FileNotFoundError(f"Missing artifact: {path}")

        self.model = Autoencoder().to(self.device)

        self.model.load_state_dict(
            torch.load(
                MODEL_PATH,
                map_location=self.device,
            )
        )

        self.model.eval()

        self.scaler_min = np.load(SCALER_MIN_PATH)
        self.scaler_scale = np.load(SCALER_SCALE_PATH)
        self.threshold = float(np.load(THRESHOLD_PATH)[0])

        self._loaded = True

        print(
            f"[ModelService] Loaded. Threshold={self.threshold:.6f}"
        )

    def is_loaded(self) -> bool:
        """
        Returns whether the model and required artifacts
        have been successfully loaded.
        """
        return self._loaded

    def scale(self, sequence: np.ndarray) -> np.ndarray:
        return (sequence - self.scaler_min) * self.scaler_scale

    def predict(self, sequence: np.ndarray) -> dict:
        """
        sequence: raw 1D array of length INPUT_DIM.

        Returns:
            reconstruction error
            anomaly flag
            threshold
            reconstructed signal
        """

        scaled = self.scale(sequence).astype(np.float32)

        x = torch.tensor(scaled).unsqueeze(0).to(self.device)

        with torch.no_grad():
            reconstructed = self.model(x)

            error = torch.mean(
                (reconstructed - x) ** 2
            ).item()

        return {
            "reconstruction_error": error,
            "is_anomaly": error > self.threshold,
            "threshold": self.threshold,
            "reconstructed": reconstructed.squeeze(0).numpy().tolist(),
        }


# Singleton instance shared across the app
model_service = ModelService()