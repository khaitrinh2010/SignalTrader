import asyncio
from websocket_client import listen_to_binance
from publisher import publish_to_redis

REDIS_CHANNEL = "market_data"

async def main():
    async for data in listen_to_binance():
        publish_to_redis(REDIS_CHANNEL, data)

if __name__ == "__main__":
    asyncio.run(main())