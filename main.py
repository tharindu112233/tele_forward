import nest_asyncio
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
from telethon import TelegramClient
from telethon.sessions import StringSession

# Apply the nest_asyncio to handle the already running event loop
nest_asyncio.apply()

# Define your Telethon client details
api_id = '1316757'
api_hash = '8af1ed19112393e98e93e09932d5ee2b'
CHANNEL_USERNAME = 'movielokay'
BOT_TOKEN = '7746593534:AAHI-6UQ7AMltUTl_ZrkckWQcKKh4PDC0xM'

# Create a Telegram client using Telethon
telethon_client = TelegramClient(
    StringSession('1BVtsOKwBuyYZCRmMOOJqmyT4RMLft9qPcWXEOuf1efujNdXM4yIDn8lyrjQE0mDSbBwYVwKBmaR_c-xgqUP8gmbH6WYmKYG-gmabXhgx1gaSa_NBukoj6CpyYeKr1M2g9RltROWLvlaYMHIkXUzcc8YpUK5ySpsLmwZPzsUERdrYQAHgQeIFLTSEptuJFGAU6kBZFiTeVQKCIjfoNH2YxNeNRxmOZmKHgVqNpWKNPujOa5INlNtX-Pr869-ROqq190EPExES9NIP-sXroySWdKKKw8O3ywMEvMOy4tpP3dITHpmcT7LuKmlbGQuZtzj7Skc7claFiEVOSS3y7O5fRLQcaQbWKcg='),
    api_id,
    api_hash
)

# Asynchronous function to search messages in the Telethon client
async def search_messages(query, limit=5):
    await telethon_client.start()  # Start the Telethon client
    results = []
    async for message in telethon_client.iter_messages(CHANNEL_USERNAME, search=query, limit=limit):
        first_line = message.text.split('\n')[0] if message.text else "No text available"
        first_line = re.sub(r'[\*_]', '', first_line)  # Remove '*' and '_' symbols
        link = f"https://t.me/{CHANNEL_USERNAME}/{message.id}"
        results.append({"first_line": first_line, "link": link})
    return results

# Define bot command handler
async def search_handler(update, context):
    query = ' '.join(context.args)  # Get the search query from the user message
    if not query:
        await update.message.reply_text("Please provide a search term. Usage: /search <keyword>")
        return

    # Search the channel using Telethon
    results = await search_messages(query)

    if not results:
        await update.message.reply_text(f"No results found for '{query}'.")
    else:
        buttons = []
        for result in results:
            # Create a button for each link
            buttons.append([InlineKeyboardButton(result['first_line'], url=result['link'])])

        # Send the results as a message with buttons
        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text("🔍 Search Results:", reply_markup=reply_markup)

# Main function to run the bot
async def main():
    # Initialize the application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handler for search
    application.add_handler(CommandHandler('search', search_handler))

    # Start polling for updates
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
