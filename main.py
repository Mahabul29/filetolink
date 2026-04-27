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

# ── Build the client ──────────────────────────────────────────────────────────
# Use STRING_SESSION if provided (avoids re-auth on every restart),
# otherwise fall back to BOT_TOKEN.
app = Client(
    "filetolink",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN if not STRING_SESSION else None,
    session_string=STRING_SESSION if STRING_SESSION else None
)

# ── Register handlers ─────────────────────────────────────────────────────────
app.on_message(filters.command("start") & filters.private)(start_cmd)
app.on_message(
    filters.private & (
        filters.document |
        filters.video    |
        filters.audio    |
        filters.photo
    )
)(file_handler)

# ── Entry point ───────────────────────────────────────────────────────────────
async def main():
    async with app:
        me = await app.get_me()
        logger.info(f"✅ Bot Started as @{me.username}")

        # Verify BIN_CHANNEL — must pass before files can be saved
        resolved = await resolve_bin_channel(app)
        if not resolved:
            logger.error(
                "❌ BIN_CHANNEL could not be resolved.\n"
                "   Files will NOT save correctly until this is fixed.\n"
                "   See the checklist printed above."
            )
            # We do NOT exit — web server still starts so Koyeb health checks pass.

        # Start the aiohttp web server (required for Koyeb health checks)
        runner = await web_server()
        logger.info(f"✅ Web server started successfully on port 8080")

        try:
            await asyncio.Event().wait()   # Keep running forever
        finally:
            await runner.cleanup()
            logger.info("🛑 Web server stopped cleanly")

if __name__ == "__main__":
    asyncio.run(main())
    
