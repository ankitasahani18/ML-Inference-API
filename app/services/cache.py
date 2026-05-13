import json
import redis.asyncio as redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def make_key(text: str):
    return f"prediction:{text}"

async def get_cache(text):
    key = make_key(text)
    return await r.get(key)

async def set_cache(text, value):
    key = make_key(text)
    await r.set(key, value, ex=3600)