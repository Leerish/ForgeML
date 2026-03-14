from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
import sys
import pandas as pd
from prefect import flow, task

from libs.common.config import settings
from libs.common.storage import upload_file
from libs.common.data_registry import make_manifest, append_manifest, next_version
from libs.quality.validator import validate_credit_risk_df
from libs.quality.reporting import write_validation_report


@task
def read_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return pd.read_csv(path)


@task
def validate_data(df: pd.DataFrame, dataset_name: str) -> dict:
    if dataset_name == "credit_risk":
        report = validate_credit_risk_df(df)
    else:
        raise ValueError(f"No validator configured for dataset: {dataset_name}")

    report_path = write_validation_report(report, dataset_name)
    report["report_path"] = report_path

    if not report["success"]:
        raise ValueError(
            f"Validation failed for dataset={dataset_name}. "
            f"See report: {report_path}"
        )

    return report


@task
def write_tmp_csv(df: pd.DataFrame, out_path: str) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path


@task
def upload_dataset(local_path: str, dataset_name: str, version: str) -> str:
    key = f"datasets/{dataset_name}/{version}/data.csv"
    return upload_file(local_path, settings.S3_DATASETS_BUCKET, key)


@task
def register_dataset(dataset_name: str, s3_uri: str, local_path: str, df: pd.DataFrame) -> dict:
    schema = {c: str(df[c].dtype) for c in df.columns}
    m = make_manifest(
        dataset_name=dataset_name,
        s3_uri=s3_uri,
        local_path=local_path,
        rows=int(df.shape[0]),
        cols=int(df.shape[1]),
        schema=schema,
        metadata={"format": "csv"},
    )
    append_manifest(m)
    return {
        "dataset": dataset_name,
        "version": m.version,
        "s3_uri": s3_uri,
        "rows": m.rows,
        "cols": m.cols,
    }


@flow(name="forgeml-ingest")
def ingest_flow(dataset_name: str, source_csv: str):
    df = read_csv(source_csv)

    validation = validate_data(df, dataset_name)
    print(f"Validation passed. Report: {validation['report_path']}")

    tmp_path = write_tmp_csv(df, f"./tmp/{dataset_name}_latest.csv")
    version = next_version(dataset_name)
    s3_uri = upload_dataset(tmp_path, dataset_name, version)
    result = register_dataset(dataset_name, s3_uri, tmp_path, df)
    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python -m services.orchestrator.flows.ingest <dataset_name> <source_csv>")

    print(ingest_flow(sys.argv[1], sys.argv[2]))