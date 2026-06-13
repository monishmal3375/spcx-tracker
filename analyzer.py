import time
from datetime import datetime

import yfinance as yf

TARGET_PRICE = 80.00
TICKER = "SPCX"


def _na_data():
    """Safe placeholder so emails still send (saying 'data unavailable') if Yahoo is down."""
    return {
        "ticker": TICKER,
        "current_price": "N/A",
        "prev_close": "N/A",
        "day_change": 0,
        "day_change_pct": 0,
        "week_high": "N/A",
        "week_low": "N/A",
        "volume": 0,
        "avg_volume": 0,
        "target_price": TARGET_PRICE,
        "distance_to_target": 0,
        "pct_to_target": 0,
        "target_hit": False,
        "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
    }


def _fetch_history():
    """Use the chart/history endpoint (tolerant of cloud IPs) instead of stock.info
    (quoteSummary), which Yahoo rate-limits with HTTP 429 from datacenter IPs.
    Retries with backoff to ride out transient 429s."""
    last_err = None
    for attempt in range(5):
        try:
            stock = yf.Ticker(TICKER)
            hist = stock.history(period="1mo")
            if hist is not None and not hist.empty:
                return stock, hist
            last_err = "empty history"
        except Exception as e:  # noqa: BLE001
            last_err = e
        time.sleep(4 * (attempt + 1))
    print(f"get_stock_data: could not fetch data after retries ({last_err})")
    return None, None


def get_stock_data():
    stock, hist = _fetch_history()
    if hist is None or hist.empty:
        return _na_data()

    current_price = float(hist["Close"].iloc[-1])
    prev_close = float(hist["Close"].iloc[-2]) if len(hist) >= 2 else current_price

    # Prefer a fresher intraday price from fast_info (also chart-endpoint based) if available.
    try:
        lp = getattr(stock.fast_info, "last_price", None)
        if lp:
            current_price = float(lp)
    except Exception:  # noqa: BLE001
        pass

    day_change = current_price - prev_close
    day_change_pct = (day_change / prev_close * 100) if prev_close else 0
    week_high = float(hist["High"].tail(5).max())
    week_low = float(hist["Low"].tail(5).min())
    volume = int(hist["Volume"].iloc[-1]) if not hist["Volume"].empty else 0
    avg_volume = int(hist["Volume"].mean()) if not hist["Volume"].empty else 0
    distance_to_target = current_price - TARGET_PRICE
    pct_to_target = (distance_to_target / TARGET_PRICE * 100) if TARGET_PRICE else 0

    return {
        "ticker": TICKER,
        "current_price": round(current_price, 2),
        "prev_close": round(prev_close, 2),
        "day_change": round(day_change, 2),
        "day_change_pct": round(day_change_pct, 2),
        "week_high": round(week_high, 2),
        "week_low": round(week_low, 2),
        "volume": volume,
        "avg_volume": avg_volume,
        "target_price": TARGET_PRICE,
        "distance_to_target": round(distance_to_target, 2),
        "pct_to_target": round(pct_to_target, 2),
        "target_hit": current_price <= TARGET_PRICE,
        "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
    }


def get_recommendation(data):
    price = data["current_price"]
    change_pct = data["day_change_pct"]
    pct_to_target = data["pct_to_target"]
    volume = data["volume"]
    avg_volume = data["avg_volume"]
    volume_ratio = volume / avg_volume if avg_volume > 0 else 1
    if price == "N/A":
        return "WAIT", "Unable to retrieve current data. Check back later."
    if price <= TARGET_PRICE:
        return "BUY NOW", f"SPCX has reached your $80 target! Current price is ${price}."
    if pct_to_target <= 10:
        return "WATCH CLOSELY", f"SPCX is only {abs(pct_to_target):.1f}% above your $80 target (${price})."
    if change_pct <= -5:
        if pct_to_target <= 25:
            return "APPROACHING - PREPARE", f"SPCX is dropping ({change_pct:.1f}% today) and is {abs(pct_to_target):.1f}% from your target."
        return "DROPPING - MONITOR", f"SPCX is down {abs(change_pct):.1f}% today."
    if volume_ratio > 2:
        return "HIGH ACTIVITY - WATCH", f"Unusual volume today ({volume_ratio:.1f}x average)."
    return "HOLD OFF", f"SPCX is at ${price}, which is {abs(pct_to_target):.1f}% above your $80 target. Wait for a dip."


def get_spacex_context():
    return {
        "ipo_price": 135,
        "first_day_close": 160.95,
        "key_facts": [
            "Starlink is SpaceX's only currently profitable segment",
            "SpaceX lost $4.9B in 2025 - investing heavily in Starship",
            "Elon Musk controls 80%+ of voting power (dual-class shares)",
            "Raised $75B in the largest IPO in history",
            "Bearish analysts set a floor target of ~$75/share",
            "Bull case: $200+ if Starlink dominates satellite internet globally",
        ],
        "why_80_matters": "The $80 target is a ~41% drop from IPO price - where fundamental valuation models suggest fair value. Bearish Wall Street analysts cite $75 as downside. Buying at $80 means getting SpaceX at a discount to even the pessimistic forecasts.",
    }
