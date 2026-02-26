from dotenv import load_dotenv
load_dotenv()
from services.binance_api import get_close_prices
from analysis.indicators import get_signal


prices = get_close_prices("BTCUSDT")
signal = get_signal(prices)

print(signal)