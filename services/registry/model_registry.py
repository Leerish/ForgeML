import json
from pathlib import Path

REGISTRY_PATH = Path("./registry/models.jsonl")
print("MODEL REGISTRY PATH:", REGISTRY_PATH.resolve())

def read_registry():

    if not REGISTRY_PATH.exists():
        return []

    lines = REGISTRY_PATH.read_text().splitlines()

    return [json.loads(l) for l in lines if l.strip()]


def get_production_model(model_name):

    records = read_registry()

    for r in records[::-1]:
        if r["model_name"] == model_name and r["stage"] == "production":
            return r

    return None


def register_model(record):

    with open(REGISTRY_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")