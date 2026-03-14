from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

from services.api.app.model_loader import get_model


REGISTRY_PATH = Path("./registry/credit_risk.jsonl")


def get_latest_dataset_version() -> str:
    if not REGISTRY_PATH.exists():
        return "unknown"

    lines = [line.strip() for line in REGISTRY_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return "unknown"

    latest = json.loads(lines[-1])
    return latest.get("version", "unknown")


def predict_credit_risk(features: dict) -> dict:
    model = get_model()

    payload = {
        "Age": features["Age"],
        "Sex": features["Sex"],
        "Job": features["Job"],
        "Housing": features["Housing"],
        "Saving accounts": features.get("Saving_accounts"),
        "Checking account": features.get("Checking_account"),
        "Credit amount": features["Credit_amount"],
        "Duration": features["Duration"],
        "Purpose": features["Purpose"],
    }

    df = pd.DataFrame([payload])

    pred = model.predict(df)[0]

    confidence = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(df)[0]
        confidence = float(max(probs))

    return {
        "prediction": int(pred),
        "confidence": confidence,
        "model_version": get_latest_dataset_version(),
    }