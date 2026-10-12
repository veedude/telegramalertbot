import os
import requests
import yfinance as yf

token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

if not token or not chat_id:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID secrets.")

# Fetch QQQ data
ticker = yf.Ticker("QQQ")
hist = ticker.history(period="5d")

if len(hist) < 2:
    print("Not enough price history returned by Yahoo Finance.")
    exit(0)

prev_close = hist["Close"].iloc[-2]
current_price = hist["Close"].iloc[-1]
pct_change = ((current_price - prev_close) / prev_close) * 100

print(f"Previous Close: ${prev_close:.2f}")
print(f"Current Price:  ${current_price:.2f}")
print(f"Daily Change:   {pct_change:.2f}%")

# Threshold set to -0.25% for testing (change to -1.0 once verified)
THRESHOLD = -0.25

if pct_change <= THRESHOLD:
    print(f"Threshold met ({pct_change:.2f}% <= {THRESHOLD}%). Sending Telegram message...")
    alert_payload = {
        "chat_id": chat_id,
        "text": f"🚨 Nasdaq Crash Alert: QQQ is down {pct_change:.2f}% today (Price: ${current_price:.2f})"
    }
    res = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=alert_payload)
    res.raise_for_status()
    print("Telegram message delivered successfully!")
else:
    print(f"Threshold not met ({pct_change:.2f}% > {THRESHOLD}%). No alert sent.")
