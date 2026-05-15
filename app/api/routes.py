import json
from fastapi import APIRouter, Depends, Request
from app.models.schemas import PredictRequest, PredictResponse

from app.services.inference import predict
from app.services.cache import get_cache, set_cache

from app.core.deps import get_current_user
from app.core.limiter import limiter

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
@limiter.limit("5/minute")
async def predict_route(
    request: Request,
    req: PredictRequest,
    user: str = Depends(get_current_user)
):
    cached = await get_cache(req.text)
    if cached:
        return PredictResponse(result=json.loads(cached), cache=True)

    result = await predict(req.text)

    await set_cache(req.text, result)

    return PredictResponse(result=result, cache=False)