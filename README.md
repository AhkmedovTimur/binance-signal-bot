# Binance Signal Bot

A mini backend system for crypto trend analysis using Binance API and Telegram interface.

## Architecture

- `services/` – external API integration (Binance)
- `analysis/` – signal calculation logic (MA strategy)
- `bot.py` – Telegram interface layer
- `config.py` – supported symbols configuration
- `.env` – environment variables (secrets)

## Features

- Fetches real-time market data from Binance
- Calculates Moving Average (MA) signals
- Detects trend direction (UP / DOWN / SIDEWAYS)
- Telegram interface with interactive buttons

## Tech Stack

- Python 3
- Binance REST API
- pyTelegramBotAPI
- Git for version control

## How to run

1. Clone the repository
2. Create virtual environment
3. Install dependencies
4. Add your `.env` file with TELEGRAM_TOKEN
5. Run:

```bash
python bot.py