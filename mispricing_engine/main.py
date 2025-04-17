import time
import requests
import json
import os
import redis
from pricing_logic import detect_real_mispricing
from publisher import publish

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)

# Watch these symbols
tracked_symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

def fetch_all_premium_indexes():
    try:
        url = "https://fapi.binance.com/fapi/v1/premiumIndex"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"[Mispricing Engine] API error: {e}")
        return []

def run():
    print("[Mispricing Engine] Monitoring:", ", ".join(tracked_symbols))
    while True:
        data = fetch_all_premium_indexes()

        for item in data:
            if item["symbol"] in tracked_symbols:
                try:
                    symbol = item["symbol"]
                    mark_price = float(item["markPrice"])
                    index_price = float(item["indexPrice"])
                    timestamp = int(item["time"])
                    funding_rate = float(item.get("lastFundingRate", 0.0))
                    signal = detect_real_mispricing(symbol, index_price, funding_rate, mark_price)
                    if signal:
                        signal["timestamp"] = timestamp
                        publish("signals", signal)
                        print("[Mispricing Engine]", signal)
                except Exception as e:
                    print(f"[Mispricing Engine] Parse error: {e}")
        time.sleep(3)
if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n[Mispricing Engine] Stopped.")
