import logging
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
# 1. MAKE SURE THIS IMPORT IS CORRECT
from plugins.start import start_cmd 

app = Client("MyBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 2. REGISTER THE HANDLER HERE
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await start_cmd(client, message)

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
    
