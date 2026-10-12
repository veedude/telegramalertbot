import os
import requests
import yfinance as yf

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

# QQQ tracks the Nasdaq-100 real-time
ticker = yf.Ticker("QQQ")
hist = ticker.history(period="2d")

if len(hist) >= 2:
    prev_close = hist["Close"].iloc[-2]
    current = hist["Close"].iloc[-1]
    pct = ((current - prev_close) / prev_close) * 100

    if pct <= -1.0:
        msg = f"🚨 Nasdaq Crash Alert: QQQ is down {pct:.2f}% today (Current: ${current:.2f})"
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat_id, "text": msg},
        )
