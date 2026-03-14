import os

class Settings:
    # MinIO (S3 compatible)
    S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:9000")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "minioadmin")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "minioadmin")
    S3_DATASETS_BUCKET = os.getenv("S3_DATASETS_BUCKET", "forgeml-datasets")
    S3_ARTIFACTS_BUCKET = os.getenv("S3_ARTIFACTS_BUCKET", "forgeml-artifacts")

    # MLflow
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

    # Local registry
    REGISTRY_DIR = os.getenv("REGISTRY_DIR", "./registry")

settings = Settings()