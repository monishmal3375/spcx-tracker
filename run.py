import sys
from analyzer import get_stock_data, get_recommendation, get_spacex_context
from email_templates import morning_email, evening_email
from emailer import send_email


def morning():
    data = get_stock_data(); ctx = get_spacex_context(); rec, reason = get_recommendation(data)
    html = morning_email(data, rec, reason, ctx); urg = data.get("target_hit", False)
    sub = f"SPCX Morning — ${data['current_price']} ({data['day_change_pct']:+.2f}%)"
    if urg:
        sub = f"TARGET HIT — SPCX at ${data['current_price']} — BUY NOW"
    send_email(sub, html, is_urgent=urg)


def evening():
    data = get_stock_data(); ctx = get_spacex_context(); rec, reason = get_recommendation(data)
    html = evening_email(data, rec, reason, ctx); urg = data.get("target_hit", False)
    sub = f"SPCX Evening — ${data['current_price']} | {rec}"
    if urg:
        sub = "SPCX HIT $80 — READ NOW"
    send_email(sub, html, is_urgent=urg)


def check():
    data = get_stock_data()
    if data.get("target_hit"):
        ctx = get_spacex_context(); rec, reason = get_recommendation(data)
        html = evening_email(data, rec, reason, ctx)
        send_email(f"URGENT — SPCX HIT $80 — ${data['current_price']}", html, is_urgent=True)
    else:
        print(f"Check OK — no target hit. Current price: ${data.get('current_price')}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"
    {"morning": morning, "evening": evening, "check": check}.get(mode, morning)()
