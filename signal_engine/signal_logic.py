def analyze_order_book(data, history=[]):
    try:
        bids = data.get("b", [])
        asks = data.get("a", [])
        timestamp = data.get("E", 0)

        if not bids or not asks:
            return None

        top_bid = float(bids[0][0])
        top_ask = float(asks[0][0])
        spread = top_ask - top_bid

        # ───────────── Spread Spike ─────────────
        if spread > 80:
            return {
                "symbol": data.get("s", ""),
                "type": "ALERT",
                "confidence": 0.85,
                "reason": f"Spread spike: ${spread:.2f}",
                "timestamp": timestamp
            }

        # ───────────── Buy/Sell Walls ─────────────
        bid_volume = sum(float(qty) for price, qty in bids[:10] if float(price) > top_bid * 0.98)
        ask_volume = sum(float(qty) for price, qty in asks[:10] if float(price) < top_ask * 1.02)

        if bid_volume > 100:
            return {
                "symbol": data.get("s", ""),
                "type": "BUY",
                "confidence": 0.92,
                "reason": f"Buy wall detected (Top 10 = {bid_volume:.2f} BTC)",
                "timestamp": timestamp
            }

        if ask_volume > 100:
            return {
                "symbol": data.get("s", ""),
                "type": "SELL",
                "confidence": 0.92,
                "reason": f"Sell wall detected (Top 10 = {ask_volume:.2f} BTC)",
                "timestamp": timestamp
            }

        # ───────────── Order Book Imbalance (OBI) ─────────────
        if (bid_volume + ask_volume) > 0:
            obi = (bid_volume - ask_volume) / (bid_volume + ask_volume)
            if obi > 0.7:
                return {
                    "symbol": data.get("s", ""),
                    "type": "BUY",
                    "confidence": 0.88,
                    "reason": f"Strong bid-side imbalance (OBI = {obi:.2f})",
                    "timestamp": timestamp
                }
            elif obi < -0.7:
                return {
                    "symbol": data.get("s", ""),
                    "type": "SELL",
                    "confidence": 0.88,
                    "reason": f"Strong ask-side imbalance (OBI = {obi:.2f})",
                    "timestamp": timestamp
                }

        # ───────────── Momentum (5-tick delta) ─────────────
        history.append(top_bid)
        if len(history) > 5:
            recent = history[-5:]
            price_diff = max(recent) - min(recent)
            if price_diff > 150:
                return {
                    "symbol": data.get("s", ""),
                    "type": "MOMENTUM",
                    "confidence": 0.87,
                    "reason": f"Price range = ${price_diff:.2f} (last 5 ticks)",
                    "timestamp": timestamp
                }

    except Exception as e:
        print(f"[Logic]: Error: {e}")

    return {
        "symbol": data.get("s", ""),
        "type": "NO_SIGNAL",
        "confidence": 0.0,
        "reason": "No valid signal detected",
        "timestamp": data.get("E", 0)
    }
