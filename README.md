# Cointracker

Cointracker is a simple email alert service for Bitcoin (BTC) and Ethereum (ETH).
It periodically polls market data from the CoinGecko API and notifies you when
several bearish indicators align.

## Description

The script fetches price history for BTC and ETH, calculates a 14‑day Relative
Strength Index (RSI) and the 200‑day moving average, and reads the Fear & Greed
Index.  If prices are falling toward major support with a weak RSI and the
market is in a state of fear, an email alert is sent.

## Installation

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Export the necessary environment variables:

   ```bash
   export ALERT_RECIPIENTS="me@example.com"
   export SMTP_HOST="smtp.example.com"
   export SMTP_PORT="587"
   export SMTP_USER="user"
   export SMTP_PASS="password"
   # optional
   export ALERT_FROM="alerts@example.com"
   export CHECK_INTERVAL="3600"
   ```

2. Run the alert service:

   ```bash
   python app/alert_service.py
   ```

## Features

- Fetch current BTC and ETH prices from CoinGecko
- Calculate the 14‑day RSI and the 200‑day moving average
- Retrieve the Fear & Greed Index
- Send email notifications when bearish indicators align

## Future improvements

- Support additional cryptocurrencies
- Provide command‑line arguments for thresholds and coins
- Optionally log alerts to a file or database

