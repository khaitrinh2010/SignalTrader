def analyze_order_book(data, history=[]):
    try:
        bids = data.get("b", [])
        asks = data.get("a", [])
        timestamp = data.get("E", 0)  # E = event time from Binance
        if not bids or not asks:
            return None
        top_bid = float(bids[0][0])
        top_ask = float(asks[0][0])
        spread = top_ask - top_bid
        if spread > 80:
            return {
                "type": "ALERT",
                "confidence": 0.85,
                "reason": f"Spread spike detected: ${spread:.2f}",
                "timestamp": timestamp
            }
        total_bid_volume = 0.0
        for price, qty in bids[:10]:
            if float(price) > top_bid * 0.98:
                total_bid_volume += float(qty)

        if total_bid_volume > 100: #many people are buying
            return {
                "type": "BUY",
                "confidence": 0.92,
                "reason": f"Buy wall detected (Volume ≈ {total_bid_volume:.2f} BTC)",
                "timestamp": timestamp
            }

        total_ask_volume = 0.0
        for price, qty in asks[:10]:  # Top 10 ask levels
            if float(price) < top_ask * 1.02:  # Within 2% of top ask
                total_ask_volume += float(qty)

        if total_ask_volume > 100: #many people are selling
            return {
                "type": "SELL",
                "confidence": 0.92,
                "reason": f"Sell wall detected (Volume ≈ {total_ask_volume:.2f} BTC)",
                "timestamp": timestamp
            }

        history.append(top_bid)
        if len(history) > 5:
            recent = history[-5:]  # Last 5 top bids
            price_diff = max(recent) - min(recent)
            if price_diff > 150:
                return {
                    "type": "MOMENTUM",
                    "confidence": 0.87,
                    "reason": f"Top bid moved ${price_diff:.2f} in 5 updates",
                    "timestamp": timestamp
                }

    except Exception as e:
        print(f"Error analyzing order book: {e}")

    return {
        "type": "NO_SIGNAL",
        "confidence": 0.0,
        "reason": "No significant signal detected",
        "timestamp": data.get("E", 0)
    }
