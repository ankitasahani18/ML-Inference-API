import json
import redis.asyncio as redis
from app.core.config import settings

r = redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)

def make_key(text: str):
    return f"prediction:{text}"

async def get_cache(text):
    key = make_key(text)
    return await r.get(key)

async def set_cache(text, value):
    key = make_key(text)
    await r.set(key, json.dumps(value), ex=3600)