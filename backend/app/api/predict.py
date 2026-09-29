import numpy as np
from fastapi import APIRouter, HTTPException

from app.schemas.prediction import SequenceInput, PredictionOutput
from app.services.model_service import model_service

router = APIRouter(prefix="/api", tags=["prediction"])


@router.post("/predict", response_model=PredictionOutput)
def predict(payload: SequenceInput):
    try:
        sequence = np.array(payload.sequence, dtype=np.float32)
        result = model_service.predict(sequence)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))