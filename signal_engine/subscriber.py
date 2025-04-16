import redis
import json
import os
import asyncio

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe("market_data")

async def subscribe_to_market_data():
    loop = asyncio.get_event_loop()
    while True:
        message = await loop.run_in_executor(None, pubsub.get_message)
        if message:
            try:
                data = json.loads(message["data"])
                yield data
            except Exception as e:
                print(f"[Subscriber]: Failed to parse: {e}")
        await asyncio.sleep(1) # Avoid busy waiting