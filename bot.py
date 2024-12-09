from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
import nest_asyncio
import re
from telethon.sessions import StringSession

api_id = '1316757'
api_hash = '8af1ed19112393e98e93e09932d5ee2b'
CHANNEL_USERNAME = 'movielokay'
BOT_TOKEN = '7746593534:AAHI-6UQ7AMltUTl_ZrkckWQcKKh4PDC0xM'


# Apply the nest_asyncio to handle the already running event loop
nest_asyncio.apply()

# Create a Telegram client
telethon_client = TelegramClient(StringSession('1BVtsOKwBuyYZCRmMOOJqmyT4RMLft9qPcWXEOuf1efujNdXM4yIDn8lyrjQE0mDSbBwYVwKBmaR_c-xgqUP8gmbH6WYmKYG-gmabXhgx1gaSa_NBukoj6CpyYeKr1M2g9RltROWLvlaYMHIkXUzcc8YpUK5ySpsLmwZPzsUERdrYQAHgQeIFLTSEptuJFGAU6kBZFiTeVQKCIjfoNH2YxNeNRxmOZmKHgVqNpWKNPujOa5INlNtX-Pr869-ROqq190EPExES9NIP-sXroySWdKKKw8O3ywMEvMOy4tpP3dITHpmcT7LuKmlbGQuZtzj7Skc7claFiEVOSS3y7O5fRLQcaQbWKcg='), api_id, api_hash)

# Asynchronous function to search messages
async def search_messages(query, limit=5):
    await telethon_client.start()  # Start the Telethon client
    results = []
    async for message in telethon_client.iter_messages(CHANNEL_USERNAME, search=query, limit=limit):
        first_line = message.text.split('\n')[0] if message.text else "No text available"
        # Remove '*' and '_' from the text
        first_line = re.sub(r'[\*_]', '', first_line)  # Removes * and _ symbols
        link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
        results.append({"first_line": first_line, "link": link})
    return results

# Define bot command handler
def search_handler(update, context):
    query = ' '.join(context.args)  # Get the search query from the user message
    if not query:
        update.message.reply_text("Please provide a search term. Usage: /search <keyword>")
        return

    # Search the channel using Telethon
    results = telethon_client.loop.run_until_complete(search_messages(query))

    if not results:
        update.message.reply_text(f"No results found for '{query}'.")
    else:
        buttons = []
        for result in results:
            # Create a button for each link
            buttons.append([
                InlineKeyboardButton(result['first_line'], url=result['link'])
            ])

        # Send the results as a message with buttons only (no extra text)
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text("🔍 Search Results:", reply_markup=reply_markup)

# Main function to run the bot
def main():
    # Initialize Telegram bot
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handler for search
    dp.add_handler(CommandHandler('search', search_handler))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
