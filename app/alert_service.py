import os
import time
import smtplib
from email.message import EmailMessage
import requests

COINS = ["bitcoin", "ethereum"]
API_BASE = "https://api.coingecko.com/api/v3"
FEAR_GREED_URL = "https://api.alternative.me/fng/"


def get_prices():
    ids = ",".join(COINS)
    r = requests.get(f"{API_BASE}/simple/price", params={"ids": ids, "vs_currencies": "usd"})
    r.raise_for_status()
    data = r.json()
    return {coin: data[coin]["usd"] for coin in COINS}


def get_price_history(coin: str, days: int = 200):
    r = requests.get(
        f"{API_BASE}/coins/{coin}/market_chart",
        params={"vs_currency": "usd", "days": days},
    )
    r.raise_for_status()
    return [point[1] for point in r.json()["prices"]]


def calculate_rsi(prices, period: int = 14):
    if len(prices) < period + 1:
        return None
    deltas = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def fear_greed_index():
    r = requests.get(FEAR_GREED_URL, params={"limit": 1})
    r.raise_for_status()
    return int(r.json()["data"][0]["value"])


def send_email(subject: str, body: str):
    recipients = [e.strip() for e in os.environ.get("ALERT_RECIPIENTS", "").split(",") if e.strip()]
    if not recipients:
        print("No recipients configured")
        return
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.environ.get("ALERT_FROM", "alerts@example.com")
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)

    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    with smtplib.SMTP(host, port) as s:
        s.starttls()
        if user:
            s.login(user, password)
        s.send_message(msg)


def check_conditions():
    prices = get_prices()
    messages = []
    for coin in COINS:
        history = get_price_history(coin, days=200)
        rsi = calculate_rsi(history[-15:])
        ma200 = sum(history) / len(history)
        price = prices[coin]
        recent_high = max(history[-60:])
        price_drop = (recent_high - price) / recent_high * 100
        near_support = price <= ma200 * 1.02
        if rsi and 30 <= rsi <= 35 and price_drop >= 25 and near_support:
            messages.append(
                f"{coin.capitalize()} price ${price:.2f}, RSI {rsi:.1f}, down {price_drop:.1f}% from 60-day high."
            )

    fng = fear_greed_index()
    if messages and fng < 25:
        body = "\n".join(messages) + f"\nFear & Greed Index: {fng}"
        send_email("Crypto Alert", body)


def main():
    interval = int(os.environ.get("CHECK_INTERVAL", "3600"))
    while True:
        try:
            check_conditions()
        except Exception as exc:  # noqa: BLE001
            print("Error:", exc)
        time.sleep(interval)


if __name__ == "__main__":
    main()
