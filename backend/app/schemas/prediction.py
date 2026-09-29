from pydantic import BaseModel, Field, field_validator

from app.core.config import INPUT_DIM


class SequenceInput(BaseModel):
    sequence: list[float] = Field(..., description=f"Time series of length {INPUT_DIM}")

    @field_validator("sequence")
    @classmethod
    def check_length(cls, v):
        if len(v) != INPUT_DIM:
            raise ValueError(f"Sequence must have exactly {INPUT_DIM} values, got {len(v)}")
        return v


class PredictionOutput(BaseModel):
    reconstruction_error: float
    is_anomaly: bool
    threshold: float
    reconstructed: list[float]


class BatchPredictionOutput(BaseModel):
    results: list[PredictionOutput]
    total: int
    anomalies_found: int