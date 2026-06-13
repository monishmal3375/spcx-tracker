# SPCX Tracker

Emails a SpaceX (NASDAQ: SPCX) stock brief twice a day and an instant alert if SPCX drops to $80.
Runs entirely on GitHub Actions (free) — no server, works with your laptop off.

## Schedule (UTC cron → US Eastern)
- `0 12 * * *`  → 8:00 AM ET morning brief
- `0 22 * * *`  → 6:00 PM ET evening analysis
- `30 * * * *`  → hourly $80 target check

> Cron is UTC and does not follow daylight saving. Times above are correct for EDT (summer).
> In winter (EST) they shift one hour earlier; bump 12→13 and 22→23 if you want exact times year-round.

## Required repository secrets (Settings → Secrets and variables → Actions)
| Secret | Value |
|---|---|
| `GMAIL_ADDRESS` | your Gmail address |
| `DAD_EMAIL` | recipient's email |
| `GMAIL_APP_PASSWORD` | 16-char Gmail App Password (not your login password) |

## Test it
Actions tab → SPCX Tracker → "Run workflow" → sends a morning email immediately.
