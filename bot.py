import logging
import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, BIN_CHANNEL, STRING_SESSION
from plugins.start import start_cmd
from plugins.files import file_handler
from web.server import web_server
from utils.channel import resolve_bin_channel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Client(
    "filetolink",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN if not STRING_SESSION else None,
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

        resolved = await resolve_bin_channel(app)
        if not resolved:
            logger.error("❌ BIN_CHANNEL could not be resolved. Files may not save correctly.")

        runner = await web_server()
        logger.info(f"🌐 Web server started")

        try:
            await asyncio.Event().wait()
        finally:
            await runner.cleanup()
            logger.info("🛑 Web server stopped cleanly")

if __name__ == "__main__":
    asyncio.run(main())
