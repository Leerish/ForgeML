from __future__ import annotations

from typing import Tuple, List
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


TARGET_COLUMN = "Risk"


def prepare_credit_risk_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare raw dataframe for model training.

    Notes:
    - Drops the index-like column 'Unnamed: 0' if present
    - Creates a binary target column 'Risk' from Credit amount
      purely for platform demonstration purposes
    """
    df = df.copy()

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Demo target:
    # High credit amount => 1, else 0
    # This is a placeholder to make the ML platform trainable end-to-end.
    if TARGET_COLUMN not in df.columns:
        median_amount = df["Credit amount"].median()
        df[TARGET_COLUMN] = (df["Credit amount"] > median_amount).astype(int)

    return df


def get_feature_lists(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    feature_df = df.drop(columns=[TARGET_COLUMN])

    numeric_features = feature_df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = feature_df.select_dtypes(include=["object"]).columns.tolist()

    return numeric_features, categorical_features


def build_preprocessor(df: pd.DataFrame) -> ColumnTransformer:
    numeric_features, categorical_features = get_feature_lists(df)

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    return preprocessor