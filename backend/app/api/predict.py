import io
import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File, Query

from app.core.config import INPUT_DIM
from app.schemas.prediction import SequenceInput, PredictionOutput, BatchPredictionOutput
from app.services.model_service import model_service

router = APIRouter(prefix="/api", tags=["prediction"])

@router.get("/models")
def list_models():
    return {"models": list(model_service.models.keys())}

@router.post("/predict", response_model=PredictionOutput)
def predict(payload: SequenceInput):
    try:
        sequence = np.array(payload.sequence, dtype=np.float32)
        return model_service.predict(sequence, model_name=payload.model)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/upload", response_model=BatchPredictionOutput)
async def predict_from_csv(file: UploadFile = File(...), model: str = Query(default="dense")):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported")

    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content), header=None)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not parse CSV")

    if df.shape[1] != INPUT_DIM:
        raise HTTPException(status_code=400, detail=f"Expected {INPUT_DIM} columns, got {df.shape[1]}")

    try:
        results = [
            model_service.predict(row.to_numpy(dtype=np.float32), model_name=model)
            for _, row in df.iterrows()
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    anomalies = sum(1 for r in results if r["is_anomaly"])
    return {"results": results, "total": len(results), "anomalies_found": anomalies}