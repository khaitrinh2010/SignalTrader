import asyncio
from subscriber import subscribe_to_market_data
from signal_logic import analyze_order_book
from publisher import publish

SIGNAL_CHANNEL = "signals"

history = []

async def run():
    async for data in subscribe_to_market_data():
        signal = analyze_order_book(data, history)
        if signal:
            print(f"[Signal Engine] Signal: {signal}")
            publish(SIGNAL_CHANNEL, signal)

if __name__ == "__main__":
    asyncio.run(run())