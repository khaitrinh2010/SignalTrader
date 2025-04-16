import websockets
import asyncio
import json

async def listen_to_binance():
    url = "wss://stream.binance.com:9443/ws/btcusdt@depth"
    print(f"[WebSocket] Connecting to {url}...")
    try:
        async with websockets.connect(url) as ws:
            print("[WebSocket] ✅ Connected to Binance.")
            async for message in ws:
                data = json.loads(message)
                yield data
    except Exception as e:
        print(f"[WebSocket] ❌ Connection error: {e}")
        await asyncio.sleep(5)  # backoff before retry
