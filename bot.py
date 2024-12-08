from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from decouple import config

BOT_API_KEY = config("BOT_API")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        channel_2_msg_id = context.args[0]
        post_url = f'https://t.me/newtest020/{channel_2_msg_id}'
        keyboard = [[InlineKeyboardButton("Go to Channel 2 Post", url=post_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Click to go to the post in Channel 2:', reply_markup=reply_markup)
    else:
        await update.message.reply_text("No message ID provided!")

async def main():
    application = Application.builder().token(BOT_API_KEY).build()
    application.add_handler(CommandHandler("start", start))
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
