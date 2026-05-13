from pydantic import BaseModel

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    result: str
    cache: bool