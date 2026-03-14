from __future__ import annotations

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

from services.api.app.schemas import CreditRiskRequest, PredictionResponse
from services.api.app.predict import predict_credit_risk
from services.api.app.model_loader import get_model, get_model_metadata


app = FastAPI(
    title="ForgeML Inference API",
    version="1.0.0",
    description="Week 6 production-ready inference service for ForgeML",
)

Instrumentator().instrument(app).expose(app)


@app.on_event("startup")
def startup_event():
    get_model()


@app.get("/health")
def health():
    try:
        get_model()
        return {"status": "ok", "model_loaded": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model-info")
def model_info():
    try:
        meta = get_model_metadata()
        return {
            "status": "ok",
            "production_model": meta,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: CreditRiskRequest):
    try:
        return predict_credit_risk(payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))