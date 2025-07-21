# Cointracker

Cointracker is a simple alert service for tracking Bitcoin (BTC) and Ethereum (ETH) market conditions. The provided script periodically fetches market data and can send email notifications when several bearish indicators align.

## Features

- Fetches current BTC and ETH prices from the CoinGecko API
- Calculates the 14‑day Relative Strength Index (RSI) and the 200‑day moving average
- Retrieves the Fear & Greed Index
- Sends email alerts when:
  - RSI is between 30 and 35
  - Prices are down 25% or more from recent highs
  - Fear & Greed Index is below 25
  - Prices are near the 200‑day moving average (acting as major support)

## Setup

1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables for your SMTP server and recipients:
   - `ALERT_RECIPIENTS`: comma‑separated list of email addresses
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`
   - Optional: `ALERT_FROM` and `CHECK_INTERVAL` (seconds between checks)
4. Run the alert service:
   ```bash
   python app/alert_service.py
   ```

The script will check conditions on each interval and send an email if all thresholds are met.
