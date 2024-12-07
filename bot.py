from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from flask import Flask, request
import os

app = Flask(__name__)

BOT_API_KEY = os.getenv("BOT_API_KEY")  # Set this as an environment variable

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello, I am your bot!")

def handle_update(request):
    updater = Updater(BOT_API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    json_str = request.get_json(force=True)
    update = Update.de_json(json_str, updater.bot)
    dp.process_update(update)

@app.route('/webhook', methods=['POST'])
def webhook():
    handle_update(request)
    return 'OK'

if __name__ == "__main__":
    app.run(debug=True)
