from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import CORS_ORIGINS
from app.services.model_service import model_service
from app.api.predict import router as predict_router


app = FastAPI(
    title="DeepAnomaly API",
    description="Self-supervised anomaly detection for time series",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(predict_router)


@app.on_event("startup")
def load_model():
    model_service.load()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model_service.is_loaded(),
    }