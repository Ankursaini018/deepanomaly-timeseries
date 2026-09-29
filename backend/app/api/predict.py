import io
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File

from app.core.config import INPUT_DIM
from app.schemas.prediction import SequenceInput, PredictionOutput, BatchPredictionOutput
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


@router.post("/predict/upload", response_model=BatchPredictionOutput)
async def predict_from_csv(file: UploadFile = File(...)):
    """
    CSV format expected: each row = one sequence, no header,
    exactly INPUT_DIM columns.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported")

    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content), header=None)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not parse CSV")

    if df.shape[1] != INPUT_DIM:
        raise HTTPException(
            status_code=400,
            detail=f"Expected {INPUT_DIM} columns, got {df.shape[1]}"
        )

    results = []
    for _, row in df.iterrows():
        sequence = row.to_numpy(dtype=np.float32)
        results.append(model_service.predict(sequence))

    anomalies = sum(1 for r in results if r["is_anomaly"])

    return {
        "results": results,
        "total": len(results),
        "anomalies_found": anomalies,
    }