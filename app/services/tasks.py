from celery import Celery
import asyncio
from app.services.inference import _run_inference

celery = Celery(
    "worker",
    broker="redis://redis:6379/1",
    backend="redis://redis:6379/2"
)

@celery.task(bind=True, max_retries=3)
def run_inference(self, text: str):
    """
    Celery task for async inference.
    Calls _run_inference directly (sync version) since Celery
    workers are not async — no event loop available here.
    """
    try:
        return _run_inference(text)
    except Exception as exc:
        # Retry with exponential backoff on failure
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)