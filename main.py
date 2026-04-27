import logging
import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from plugins.start import start_cmd
from plugins.files import file_handler
from web.server import web_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("JavaGoatBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register Handlers
app.on_message(filters.command("start") & filters.private)(start_cmd)
app.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo))(file_handler)

async def main():
    async with app:
        # Start web server for Koyeb Health Checks
        await web_server()
        logger.info("✅ Web Server & Bot are Online!")
        
        # Keep the bot running
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
