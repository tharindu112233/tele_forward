from decouple import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_API_KEY = config("BOT_API")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the message_id passed in the URL (after "start=")
    if context.args:
        channel_2_msg_id = context.args[0]  # This will be the message_id of the post in Channel 2

        # Construct the link to the post in Channel 2
        post_url = f'https://t.me/newtest020/{channel_2_msg_id}'

        # Create the button to redirect to Channel 2's post
        keyboard = [
            [InlineKeyboardButton("Go to Channel 2 Post", url=post_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send message with the button
        await update.message.reply_text('Click to go to the post in Channel 2:', reply_markup=reply_markup)
    else:
        # In case no message_id is provided, reply with a default message
        await update.message.reply_text("No message ID provided!")

async def main():
    # Set up the Application and Dispatcher (new method)
    application = Application.builder().token(BOT_API_KEY).build()

    # Add handler for the /start command (which takes parameters)
    application.add_handler(CommandHandler("start", start))

    # Start polling for updates
    await application.run_polling()

# Run the main function directly without manually handling the event loop
if __name__ == '__main__':
    import asyncio

    # Simply run the main function within the existing event loop
    asyncio.run(main())
