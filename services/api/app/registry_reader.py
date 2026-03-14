from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_REGISTRY_PATH = BASE_DIR / "registry" / "models.jsonl"


def get_production_model_record(model_name: str = "credit_risk") -> dict | None:
    if not MODEL_REGISTRY_PATH.exists():
        return None

    lines = MODEL_REGISTRY_PATH.read_text(encoding="utf-8").splitlines()
    records = [json.loads(line) for line in lines if line.strip()]

    for record in reversed(records):
        if record.get("model_name") == model_name and record.get("stage") == "production":
            return record

    return None