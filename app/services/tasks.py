from celery import Celery

celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task
def run_inference(text):
    return text.upper()