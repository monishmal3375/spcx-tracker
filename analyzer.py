import yfinance as yf
from datetime import datetime

TARGET_PRICE = 80.00
TICKER = "SPCX"

def get_stock_data():
    stock = yf.Ticker(TICKER)
    info = stock.info
    hist = stock.history(period="5d")
    current_price = info.get("currentPrice") or info.get("regularMarketPrice") or (hist["Close"].iloc[-1] if not hist.empty else None)
    prev_close = info.get("previousClose") or (hist["Close"].iloc[-2] if len(hist) >= 2 else current_price)
    day_change = current_price - prev_close if current_price and prev_close else 0
    day_change_pct = (day_change / prev_close * 100) if prev_close else 0
    week_high = hist["High"].max() if not hist.empty else current_price
    week_low = hist["Low"].min() if not hist.empty else current_price
    volume = hist["Volume"].iloc[-1] if not hist.empty else 0
    avg_volume = hist["Volume"].mean() if not hist.empty else 0
    distance_to_target = current_price - TARGET_PRICE if current_price else 0
    pct_to_target = (distance_to_target / TARGET_PRICE * 100) if TARGET_PRICE else 0
    return {
        "ticker": TICKER,
        "current_price": round(current_price, 2) if current_price else "N/A",
        "prev_close": round(prev_close, 2) if prev_close else "N/A",
        "day_change": round(day_change, 2),
        "day_change_pct": round(day_change_pct, 2),
        "week_high": round(week_high, 2) if week_high else "N/A",
        "week_low": round(week_low, 2) if week_low else "N/A",
        "volume": int(volume),
        "avg_volume": int(avg_volume),
        "target_price": TARGET_PRICE,
        "distance_to_target": round(distance_to_target, 2),
        "pct_to_target": round(pct_to_target, 2),
        "target_hit": current_price <= TARGET_PRICE if current_price else False,
        "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p")
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
            "Bull case: $200+ if Starlink dominates satellite internet globally"
        ],
        "why_80_matters": "The $80 target is a ~41% drop from IPO price - where fundamental valuation models suggest fair value. Bearish Wall Street analysts cite $75 as downside. Buying at $80 means getting SpaceX at a discount to even the pessimistic forecasts."
    }
