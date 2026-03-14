from __future__ import annotations

from pathlib import Path
import joblib

from services.api.app.registry_reader import get_production_model_record


BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "artifacts" / "credit_model.joblib"

_model = None
_model_meta = None


def get_model():
    global _model, _model_meta

    if _model is None:
        prod = get_production_model_record("credit_risk")
        _model_meta = prod

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. Run Week 3 training first."
            )

        _model = joblib.load(MODEL_PATH)

    return _model


def get_model_metadata():
    global _model_meta
    if _model_meta is None:
        _model_meta = get_production_model_record("credit_risk")
    return _model_meta