from pydantic import BaseModel


class ModelRecord(BaseModel):

    model_name: str
    version: str
    dataset_version: str
    accuracy: float
    stage: str