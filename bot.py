import logging
import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, BIN_CHANNEL, PORT, STRING_SESSION
from plugins.start import start_cmd
from plugins.files import file_handler
from web.server import web_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Client(
    "filetolink",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    session_string=STRING_SESSION if STRING_SESSION else None
)

app.on_message(filters.command("start") & filters.private)(start_cmd)

app.on_message(
    filters.private & (
        filters.document |
        filters.video |
        filters.audio |
        filters.photo
    )
)(file_handler)

async def main():
    async with app:
        me = await app.get_me()
        logger.info(f"✅ Bot Started as @{me.username}")

        try:
            chat = await app.get_chat(BIN_CHANNEL)
            logger.info(f"✅ BIN_CHANNEL resolved: {chat.title}")
        except Exception as e:
            logger.warning(f"⚠️ BIN_CHANNEL warning: {e}")

        runner = await web_server(PORT)
        logger.info(f"🌐 Web server running on port {PORT}")

        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
