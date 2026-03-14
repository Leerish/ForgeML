from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class CreditRiskRequest(BaseModel):
    Age: int
    Sex: str
    Job: int
    Housing: str
    Saving_accounts: Optional[str] = None
    Checking_account: Optional[str] = None
    Credit_amount: float
    Duration: int
    Purpose: str


class PredictionResponse(BaseModel):
    prediction: int
    confidence: Optional[float] = None
    model_version: str