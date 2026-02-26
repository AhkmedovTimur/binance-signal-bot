import requests


BASE_URL = "https://api.binance.com/api/v3/klines"


def get_close_prices(symbol: str, interval: str = "15m", limit: int = 50) -> list[float]:
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    close_prices = [float(candle[4]) for candle in data]

    return close_prices
