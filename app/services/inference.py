import asyncio
import time
from functools import lru_cache
from loguru import logger
from transformers import pipeline

# Load model once using lru_cache — calling get_model() multiple times
# returns the same object, never reloads from disk
@lru_cache(maxsize=1)
def get_model():
    logger.info("Loading sentiment model — this takes 10-30 seconds on first run...")
    model = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        return_all_scores=False
    )
    logger.info("Model loaded successfully")
    return model

# Label map — the model returns LABEL_0/1/2, we convert to human readable
LABEL_MAP = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

async def predict(text: str) -> dict:
    """
    Run sentiment inference on input text.
    Runs the CPU-bound model in a thread pool via asyncio.to_thread
    so it doesn't block the FastAPI event loop.
    """
    start = time.perf_counter()

    # asyncio.to_thread moves the blocking model call off the event loop
    # Without this, the API freezes for every other request during inference
    result = await asyncio.to_thread(_run_inference, text)

    latency_ms = round((time.perf_counter() - start) * 1000, 2)

    logger.info(f"Inference complete | label={result['label']} score={result['score']:.4f} latency={latency_ms}ms")

    return {
        "label": result["label"],
        "score": round(result["score"], 4),
        "latency_ms": latency_ms
    }

def _run_inference(text: str) -> dict:
    """
    Synchronous inference call — runs inside a thread pool.
    Separated from predict() so asyncio.to_thread can wrap it cleanly.
    """
    model = get_model()
    raw = model(text, truncation=True, max_length=512)[0]

    # Map LABEL_0/1/2 to negative/neutral/positive
    label = LABEL_MAP.get(raw["label"], raw["label"].lower())

    return {
        "label": label,
        "score": raw["score"]
    }