from dotenv import load_dotenv
load_dotenv()
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import SUPPORTED_SYMBOLS
import os
from services.binance_api import get_close_prices
from analysis.indicators import get_signal

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = TeleBot(TOKEN)

def get_available_buttons():
	return list(SUPPORTED_SYMBOLS.keys())

def handle_symbol(symbol_name: str) -> str:
      if symbol_name not in SUPPORTED_SYMBOLS:
            return "Symbol not supported"
      symbol = SUPPORTED_SYMBOLS[symbol_name]
      prices = get_close_prices(symbol)
      signal = get_signal(prices)
      return signal

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for name in get_available_buttons():
        button = KeyboardButton(name)
        markup.add(button)
    bot.send_message(message.chat.id, "Choose crypto", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    symbol_name = message.text
    result = handle_symbol(symbol_name)
    bot.send_message(message.chat.id, result)    

if __name__ == "__main__":
    bot.infinity_polling()