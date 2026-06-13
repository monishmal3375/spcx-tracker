def get_color(pct): return "#16a34a" if pct > 0 else ("#dc2626" if pct < 0 else "#6b7280")
def get_arrow(pct): return "▲" if pct > 0 else ("▼" if pct < 0 else "—")
def rec_color(r):
    c = {"BUY NOW":"#16a34a","WATCH CLOSELY":"#d97706","APPROACHING - PREPARE":"#d97706","DROPPING - MONITOR":"#dc2626","HIGH ACTIVITY - WATCH":"#7c3aed","HOLD OFF":"#2563eb"}
    return c.get(r,"#6b7280")

def morning_email(data, rec, rec_reason, context):
    p=data["current_price"]; ch=data["day_change"]; cp=data["day_change_pct"]
    col=get_color(cp); arr=get_arrow(cp); tg=abs(data["distance_to_target"]); tp=abs(data["pct_to_target"]); rc=rec_color(rec)
    banner=""
    if data.get("target_hit"):
        banner='<tr><td style="background:#16a34a;padding:20px;text-align:center;"><p style="color:#fff;font-size:22px;font-weight:700;margin:0;">TARGET REACHED — $80 OR BELOW</p></td></tr>'
    facts="".join(f'<li style="margin:6px 0;color:#374151;font-size:14px;">{f}</li>' for f in context.get("key_facts",[]))
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="padding:24px 0;"><tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:12px;overflow:hidden;max-width:600px;">
<tr><td style="background:#0f172a;padding:28px 32px;">
<p style="color:#94a3b8;font-size:12px;margin:0;">SpaceX Stock Tracker</p>
<p style="color:#fff;font-size:24px;font-weight:700;margin:4px 0;">Good morning ☀️</p>
<p style="color:#64748b;font-size:13px;margin:4px 0;">{data["timestamp"]} · NASDAQ: SPCX</p>
</td></tr>{banner}
<tr><td style="padding:28px 32px 16px;">
<table width="100%"><tr>
<td style="background:#f8fafc;border-radius:10px;padding:20px;border:1px solid #e2e8f0;">
<p style="color:#6b7280;font-size:12px;margin:0 0 6px;">Current price</p>
<p style="font-size:40px;font-weight:700;color:#0f172a;margin:0;">${p}</p>
<p style="font-size:15px;color:{col};margin:6px 0 0;">{arr} ${abs(ch):.2f} ({abs(cp):.2f}%) today</p>
</td><td width="16"></td>
<td style="background:#f8fafc;border-radius:10px;padding:20px;border:1px solid #e2e8f0;">
<p style="color:#6b7280;font-size:12px;margin:0 0 6px;">Your $80 target</p>
<p style="font-size:40px;font-weight:700;color:#0f172a;margin:0;">$80</p>
<p style="font-size:15px;color:#6b7280;margin:6px 0 0;">${tg:.2f} ({tp:.1f}%) away</p>
</td></tr></table></td></tr>
<tr><td style="padding:0 32px 24px;">
<div style="border-left:4px solid {rc};background:#f8fafc;padding:16px 20px;">
<p style="color:{rc};font-size:11px;font-weight:700;text-transform:uppercase;margin:0 0 4px;">Morning call</p>
<p style="font-size:16px;font-weight:700;color:{rc};margin:0 0 6px;">{rec}</p>
<p style="font-size:14px;color:#374151;margin:0;line-height:1.6;">{rec_reason}</p>
</div></td></tr>
<tr><td style="padding:0 32px 24px;">
<p style="font-size:14px;color:#374151;line-height:1.7;margin:0;">{context.get("why_80_matters","")}</p>
</td></tr>
<tr><td style="background:#f8fafc;padding:20px 32px;border-top:1px solid #e2e8f0;">
<p style="font-size:12px;color:#9ca3af;margin:0;">Evening analysis at 6 PM. Not financial advice.</p>
</td></tr></table></td></tr></table></body></html>"""

def evening_email(data, rec, rec_reason, context):
    p=data["current_price"]; ch=data["day_change"]; cp=data["day_change_pct"]
    col=get_color(cp); arr=get_arrow(cp); tg=abs(data["distance_to_target"]); tp=abs(data["pct_to_target"]); rc=rec_color(rec)
    banner=""
    if data.get("target_hit"):
        banner='<tr><td style="background:#16a34a;padding:20px 32px;text-align:center;"><p style="color:#fff;font-size:20px;font-weight:700;margin:0;">TARGET HIT — TIME TO ACT</p></td></tr>'
    facts="".join(f'<li style="margin:6px 0;color:#374151;font-size:14px;">{f}</li>' for f in context.get("key_facts",[]))
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="padding:24px 0;"><tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:12px;overflow:hidden;max-width:600px;">
<tr><td style="background:#0f172a;padding:28px 32px;">
<p style="color:#94a3b8;font-size:12px;margin:0;">SpaceX Stock Tracker · Evening Report</p>
<p style="color:#fff;font-size:24px;font-weight:700;margin:4px 0;">SPCX Daily Analysis 🛰️</p>
<p style="color:#64748b;font-size:13px;margin:4px 0;">{data["timestamp"]} · NASDAQ: SPCX</p>
</td></tr>{banner}
<tr><td style="padding:28px 32px 16px;">
<table width="100%"><tr>
<td style="background:#f8fafc;border-radius:10px;padding:20px;border:1px solid #e2e8f0;">
<p style="color:#6b7280;font-size:12px;margin:0 0 6px;">Today's close</p>
<p style="font-size:38px;font-weight:700;color:#0f172a;margin:0;">${p}</p>
<p style="font-size:15px;color:{col};margin:6px 0 0;">{arr} ${abs(ch):.2f} ({abs(cp):.2f}%) today</p>
</td><td width="16"></td>
<td style="background:#f8fafc;border-radius:10px;padding:20px;border:1px solid #e2e8f0;">
<p style="color:#6b7280;font-size:12px;margin:0 0 6px;">Buy target</p>
<p style="font-size:38px;font-weight:700;color:#0f172a;margin:0;">$80</p>
<p style="font-size:15px;color:#6b7280;margin:6px 0 0;">${tg:.2f} away ({tp:.1f}%)</p>
</td></tr></table></td></tr>
<tr><td style="padding:8px 32px 24px;">
<div style="border-left:4px solid {rc};background:#f8fafc;padding:18px 20px;">
<p style="color:{rc};font-size:11px;font-weight:700;text-transform:uppercase;margin:0 0 4px;">Tonight's recommendation</p>
<p style="font-size:18px;font-weight:700;color:{rc};margin:0 0 8px;">{rec}</p>
<p style="font-size:14px;color:#374151;margin:0;line-height:1.7;">{rec_reason}</p>
</div></td></tr>
<tr><td style="padding:0 32px 24px;">
<p style="font-size:16px;font-weight:700;color:#0f172a;margin:0 0 14px;">Bull vs Bear</p>
<table width="100%"><tr>
<td width="48%" style="background:#f0fdf4;border-radius:10px;padding:16px;border:1px solid #bbf7d0;vertical-align:top;">
<p style="color:#16a34a;font-size:12px;font-weight:700;text-transform:uppercase;margin:0 0 8px;">Bull — $200+</p>
<p style="font-size:13px;color:#374151;margin:0;line-height:1.6;">Starlink dominates global internet. Starship commercializes. Revenue surpasses $40B by 2028.</p>
</td><td width="4%"></td>
<td width="48%" style="background:#fef2f2;border-radius:10px;padding:16px;border:1px solid #fecaca;vertical-align:top;">
<p style="color:#dc2626;font-size:12px;font-weight:700;text-transform:uppercase;margin:0 0 8px;">Bear — $75</p>
<p style="font-size:13px;color:#374151;margin:0;line-height:1.6;">$4.9B loss unsustainable. P/S of 60x extreme. Musk distraction risk. IPO hype fades.</p>
</td></tr></table></td></tr>
<tr><td style="padding:0 32px 24px;">
<p style="font-size:16px;font-weight:700;color:#0f172a;margin:0 0 12px;">Key facts about SpaceX</p>
<ul style="margin:0;padding-left:20px;">{facts}</ul>
</td></tr>
<tr><td style="padding:0 32px 24px;">
<p style="font-size:16px;font-weight:700;color:#0f172a;margin:0 0 14px;">How to buy when it hits $80</p>
<table width="100%" style="border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;">
<tr><td style="padding:10px 16px;border-bottom:1px solid #e2e8f0;font-size:13px;color:#374151;"><strong style="color:#7c3aed;">1</strong> &nbsp; Open Fidelity, Schwab or Robinhood — search SPCX</td></tr>
<tr><td style="padding:10px 16px;border-bottom:1px solid #e2e8f0;font-size:13px;color:#374151;"><strong style="color:#7c3aed;">2</strong> &nbsp; Place a LIMIT order at $80 (not market order)</td></tr>
<tr><td style="padding:10px 16px;border-bottom:1px solid #e2e8f0;font-size:13px;color:#374151;"><strong style="color:#7c3aed;">3</strong> &nbsp; Only invest money you can keep for 3-5 years</td></tr>
<tr><td style="padding:10px 16px;font-size:13px;color:#374151;"><strong style="color:#7c3aed;">4</strong> &nbsp; Consider buying in portions, not all at once</td></tr>
</table></td></tr>
<tr><td style="background:#f8fafc;padding:20px 32px;border-top:1px solid #e2e8f0;">
<p style="font-size:12px;color:#9ca3af;margin:0;">Next morning report at 8 AM. Not financial advice.</p>
</td></tr></table></td></tr></table></body></html>"""
