import asyncio

async def predict(text: str):

    await asyncio.sleep(2)

    return text.upper()