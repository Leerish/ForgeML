from __future__ import annotations

from typing import Dict, Any, Tuple
import os
import json

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from services.registry.promote_model import promote_if_better

from libs.features.feature_builder import (
    TARGET_COLUMN,
    prepare_credit_risk_dataframe,
    build_preprocessor,
)


def train_credit_model(
    df: pd.DataFrame,
    dataset_name: str,
    dataset_version: str,
    experiment_name: str = "forgeml-credit-risk",
) -> Dict[str, Any]:
    """
    Train a demo binary classification model and log everything to MLflow.
    """
    os.makedirs("./artifacts", exist_ok=True)

    df = prepare_credit_risk_dataframe(df)

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    preprocessor = build_preprocessor(df)

    model_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run() as run:
        model_pipeline.fit(X_train, y_train)
        preds = model_pipeline.predict(X_test)

        metrics = {
            "accuracy": float(accuracy_score(y_test, preds)),
            "precision": float(precision_score(y_test, preds, zero_division=0)),
            "recall": float(recall_score(y_test, preds, zero_division=0)),
            "f1": float(f1_score(y_test, preds, zero_division=0)),
        }

        params = {
            "model_type": "LogisticRegression",
            "test_size": 0.2,
            "random_state": 42,
            "dataset_name": dataset_name,
            "dataset_version": dataset_version,
            "target_column": TARGET_COLUMN,
        }

        for k, v in params.items():
            mlflow.log_param(k, v)

        mlflow.log_param("num_rows", int(df.shape[0]))
        mlflow.log_param("num_cols", int(df.shape[1]))

        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        promotion = promote_if_better(
            model_name="credit_risk",
            dataset_version=dataset_version,
            accuracy=metrics["accuracy"],
        )

        feature_info = {
            "input_columns": X.columns.tolist(),
            "target_column": TARGET_COLUMN,
        }

        feature_info_path = "./artifacts/feature_info.json"
        with open(feature_info_path, "w", encoding="utf-8") as f:
            json.dump(feature_info, f, indent=2)

        local_model_path = "./artifacts/credit_model.joblib"
        joblib.dump(model_pipeline, local_model_path)

        mlflow.log_artifact(feature_info_path, artifact_path="metadata")
        mlflow.log_artifact(local_model_path, artifact_path="model_artifacts")
        mlflow.sklearn.log_model(model_pipeline, artifact_path="model")

        result = {
            "run_id": run.info.run_id,
            "experiment_name": experiment_name,
            "metrics": metrics,
            "params": params,
            "model_artifact": local_model_path,
            "promotion_result": promotion,
        }

    return result