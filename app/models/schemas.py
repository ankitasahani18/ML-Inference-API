from pydantic import BaseModel
from typing import Any

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    result: Any  # inference returns a dict: {label, score, latency_ms}
    cache: bool