from dotenv import load_dotenv
load_dotenv()
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import ReplyKeyboardRemove
from config import SUPPORTED_SYMBOLS
import os
from services.binance_api import get_close_prices
from analysis.indicators import get_signal

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = TeleBot(TOKEN)

user_states = {}

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

@bot.message_handler(func=lambda message: message.text in SUPPORTED_SYMBOLS)
def choose_symbol(message):
    chat_id = message.chat.id
    symbol_code = SUPPORTED_SYMBOLS[message.text]
    user_states[chat_id] = {"symbol": symbol_code}
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row(KeyboardButton("MA"), KeyboardButton("EMA"))

    bot.send_message(chat_id, "Choose indicator", reply_markup=markup) 

@bot.message_handler(func=lambda message: message.text in ["MA", "EMA"])
def choose_indicator(message):
     chat_id = message.chat.id
     if chat_id not in user_states:
          bot.send_message(chat_id, "Please choose a crypto first")
          return
     symbol = user_states[chat_id]["symbol"]
     indicator = message.text.lower()
     prices = get_close_prices(symbol)
     result = get_signal(prices, indicator=indicator)
     markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
     markup.row(KeyboardButton("BACK"))
     bot.send_message(chat_id, result, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "BACK")
def handle_back(message):
    chat_id = message.chat.id

    user_states.pop(chat_id, None)

    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for name in get_available_buttons():
        markup.add(KeyboardButton(name))

    bot.send_message(chat_id, "Choose crypto", reply_markup=markup)

if __name__ == "__main__":
    bot.infinity_polling()