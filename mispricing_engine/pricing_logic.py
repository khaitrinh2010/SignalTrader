import time

def detect_real_mispricing(symbol, index_price, mark_price, funding_rate=None, threshold_pct=0.0008):
    """
    Detects real-world mispricing between mark price and index price.

    Parameters:
        symbol (str): The trading pair (e.g., BTCUSDT)
        index_price (float): The fair price of the asset
        mark_price (float): The current futures mark price
        funding_rate (float or None): Optional funding rate as a decimal (e.g., 0.0001 = 0.01%)
        threshold_pct (float): Minimum deviation threshold (default: 0.08%)

    Returns:
        dict: Signal dictionary
    """
    price_diff = mark_price - index_price
    deviation = abs(price_diff) / index_price

    timestamp = int(time.time() * 1000)

    if deviation >= threshold_pct:
        signal_type = "ARBITRAGE_BUY" if price_diff < 0 else "ARBITRAGE_SELL"

        # Confidence boosted by funding rate if available
        confidence = 0.9 + deviation * 50
        if funding_rate is not None:
            confidence += abs(funding_rate) * 20

        confidence = min(confidence, 1.0)

        reason = (
            f"{symbol} mispricing: mark = ${mark_price:.2f}, index = ${index_price:.2f}, "
            f"diff = ${price_diff:.2f} ({deviation:.2%})"
        )

        if funding_rate is not None:
            reason += f", funding = {funding_rate:.5f}"

        return {
            "symbol": symbol,
            "type": signal_type,
            "confidence": round(confidence, 3),
            "reason": reason,
            "timestamp": timestamp
        }

    return {
        "symbol": symbol,
        "type": "NO_ARBITRAGE_SIGNAL",
        "confidence": 0.0,
        "reason": (
            f"No significant mispricing detected: mark = ${mark_price:.2f}, index = ${index_price:.2f}"
        ),
        "timestamp": timestamp
    }
