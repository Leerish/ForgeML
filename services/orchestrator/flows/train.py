from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import json
import os
import sys
import pandas as pd

from prefect import flow, task

from services.training.train_model import train_credit_model


@task
def read_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return pd.read_csv(path)


@task
def detect_dataset_version(dataset_name: str) -> str:
    registry_path = f"./registry/{dataset_name}.jsonl"
    if not os.path.exists(registry_path):
        return "unknown"

    with open(registry_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return "unknown"

    latest = json.loads(lines[-1])
    return latest.get("version", "unknown")


@task
def train_model_task(df: pd.DataFrame, dataset_name: str, dataset_version: str) -> dict:
    return train_credit_model(
        df=df,
        dataset_name=dataset_name,
        dataset_version=dataset_version,
    )


@flow(name="forgeml-train")
def train_flow(dataset_name: str, source_csv: str):
    df = read_csv(source_csv)
    dataset_version = detect_dataset_version(dataset_name)
    result = train_model_task(df, dataset_name, dataset_version)
    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python -m services.orchestrator.flows.train <dataset_name> <source_csv>")

    print(train_flow(sys.argv[1], sys.argv[2]))