import os
import requests
import time
import schedule
from datetime import datetime
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from keep_alive import keep_alive

# === CONFIG ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = 969702606  # Replace with your Telegram ID
COINS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
bot = Bot(token=TELEGRAM_TOKEN)
last_signal = {}

def fetch_ohlc(symbol, interval):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
    r = requests.get(url)
    data = r.json()
    return [list(map(float, [c[1], c[2], c[3], c[4]])) for c in data]

def check_signals(symbol):
    candles_15m = fetch_ohlc(symbol, "15m")
    candles_1h = fetch_ohlc(symbol, "1h")
    if candles_15m[-1][3] > candles_15m[-2][3] and candles_1h[-1][3] > candles_1h[-2][3]:
        return "STRONG BUY"
    elif candles_15m[-1][3] < candles_15m[-2][3] and candles_1h[-1][3] < candles_1h[-2][3]:
        return "STRONG SELL"
    return "NEUTRAL"

def send_signal(symbol, signal):
    price = fetch_ohlc(symbol, "15m")[-1][3]
    msg = f"🔔 *{signal}* for `{symbol}`\nEntry: ${price:.2f}\nTime: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

def scan_all():
    for coin in COINS:
        signal = check_signals(coin)
        if signal in ["STRONG BUY", "STRONG SELL"] and last_signal.get(coin) != signal:
            send_signal(coin, signal)
            last_signal[coin] = signal

def status(update, context):
    update.message.reply_text("✅ Bot is running fine!")

def last(update, context):
    msg = "\n".join([f"{k}: {v}" for k, v in last_signal.items()]) or "No signals yet."
    update.message.reply_text(msg)

def help_cmd(update, context):
    update.message.reply_text("/status - Bot status\n/lastsignal - Last signals\n/help - Commands")

def start_bot():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("lastsignal", last))
    dp.add_handler(CommandHandler("help", help_cmd))
    updater.start_polling()

keep_alive()
schedule.every(15).minutes.do(scan_all)
schedule.every(4).hours.do(lambda: bot.send_message(chat_id=CHAT_ID, text="✅ Bot is Active"))

start_bot()

while True:
    schedule.run_pending()
    time.sleep(5)
