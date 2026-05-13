from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.logging import setup_logging
from app.utils.metrics import instrument_app

from app.api.routes import router as api_router
from app.api.auth import router as auth_router

from app.core.limiter import limiter

app = FastAPI(title="ML Inference API")

setup_logging()

instrument_app(app)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

app.include_router(auth_router)
app.include_router(api_router)