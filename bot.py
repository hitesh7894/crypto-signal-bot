import time
import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import threading
import os

# === CONFIG ===
TOKEN = '7612808640:AAEm0j8gL-6dswKPHCSqt7eMi4f0L0tbEys'
CHAT_ID = '969702606'

# === INIT ===
bot = Bot(token=TOKEN)

# === SIGNAL SIMULATION (replace with real logic later) ===
def check_signals():
    while True:
        try:
            # Replace with actual indicator logic
            bot.send_message(chat_id=CHAT_ID, text="🚨 STRONG BUY Alert\n🔹Coin: ETHUSDT\n🔹Entry: 1983.20\n🔹SL: 1942.30\n🔹TP: 2043.20\n📊 Timeframe: 15m + 1h Aligned\n📍 Reason: RSI+MACD+Supertrend")
            time.sleep(900)  # wait 15 minutes before next check
        except Exception as e:
            print(f"Error sending signal: {e}")

# === COMMAND HANDLERS ===
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Crypto Signal Bot is online!")

def help_cmd(update, context):
    msg = "/status – Bot live status\n/lastsignal – Last alert\n/summary – Recent trades\n/help – Command list"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def status(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Bot is Active and Monitoring...")

def lastsignal(update, context):
    msg = "📢 Last Signal:\n🔹ETHUSDT\nSTRONG BUY\n📍 Entry: 1983.20\nSL: 1942.30 | TP: 2043.20"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

# === MAIN BOT THREAD ===
def run_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_cmd))
    dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_handler(CommandHandler('lastsignal', lastsignal))

    updater.start_polling()

    # Send heartbeat every 4 hours
    def send_heartbeat():
        while True:
            time.sleep(14400)  # 4 hours
            bot.send_message(chat_id=CHAT_ID, text="🔁 Bot is Active ✅\n⏰ Last check: Running fine.")

    threading.Thread(target=send_heartbeat).start()

    # Run signal checker
    threading.Thread(target=check_signals).start()

# === ENTRY POINT ===
if __name__ == '__main__':
    from keep_alive import keep_alive
    keep_alive()
    run_bot()
